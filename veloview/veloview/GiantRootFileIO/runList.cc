/** @file runList.cc
 *
 * @brief modify text file containing sorted list of runs
 *
 * @author Manuel Schiller <Manuel.Schiller@cern.ch>
 * @date 2014-10-24
 *
 * command line utility to add/remove a set of runs given on command line
 * to/from plain text file containing sorted list of available runs
 *
 * Care is taken to ensure that concurrent use of the utility to modify the
 * same run list file does not lead to race conditions.
 *
 * Updates to the run list file happen atomically from the point of view of any
 * application reading that file; reading the run list file is thus possible at
 * any moment, without special utilities or locking primitives, and produces a
 * consistent view of the run list at the point of time the file was opened.
 */
#include <cerrno>
#include <cstdio>
#include <cstdint>
#include <cstdlib>

#include <vector>
#include <fstream>
#include <sstream>
#include <iostream>
#include <typeinfo>
#include <algorithm>
#include <system_error>

#include <getopt.h> // getopt_long
#include <cxxabi.h> // __cxa_demangle

#include "DotLock.h"

/** @brief add/remove runs from runlist, keep runlist sorted
 *
 * @param runlist	list of runs
 * @param runs		runs to add/remove
 * @param remove	true if runs are to be removed
 *
 * @returns		true if runlist was changed
 */
static bool addRemoveRuns(std::vector<uint64_t>& runlist,
	std::vector<uint64_t>& runs, bool remove = false)
{
    // sanitise list of runs to add/remove
    if (1 < runs.size()) {
	// sort
	std::sort(std::begin(runs), std::end(runs));
	// and make sure each run number is unique
	auto it = std::unique(std::begin(runs), std::end(runs));
	if (std::end(runs) != it) runs.erase(it, std::end(runs));
    }
    bool retVal = false;
    if (!remove) {
	// add runs in runs to runlist
	auto begin = std::begin(runlist);
	for (uint64_t run: runs) {
	    begin = std::lower_bound(begin, std::end(runlist), run);
	    if (std::end(runlist) == begin) {
		// default on sorted list will be append at end
		runlist.push_back(run);
	    } else if (*begin != run) {
		// sometimes we'll have to insert "in the middle"
		// (shouldn't happen often, since runlist is sorted, and we add
		// very few runs compared to the size of the runlist)
		runlist.insert(begin, run);
	    } else {
		// already in list - do nothing
		continue;
	    }
	    retVal = true;
	}
    } else {
	// remove runs in runs from runlist
	// dp - pointer to next run to be deleted (in runs)
	// rp - read pointer, wp - write pointer (in runlist)
	auto dp = std::begin(runs);
	auto rp = std::begin(runlist), wp = std::begin(runlist);
	while (std::end(runlist) != rp) {
	    // skip ahead to lowest run number to remove
	    auto rp2 = (std::end(runs) != dp) ?
		std::lower_bound(rp, std::end(runlist), *dp) :
		std::end(runlist);
	    // if we need to move data to "close the holes", do so now
	    if (rp != wp) wp = std::copy(rp, rp2, wp);
	    else wp += rp2 - rp;
	    // next element to investigate
	    rp = rp2;
	    if (std::end(runlist) == rp) break;
	    if (*rp > *dp) {
		// *dp not found, advance *dp, find next occurrence
		++dp;
	    } else {
		// set flag that we change runlist
		retVal = true;
		// *dp found, skip it
		++rp, ++dp;
	    }
	}
	// erase the "holes"
	if (std::end(runlist) != wp) runlist.erase(wp, std::end(runlist));
    }
    return retVal;
}

/** @brief read list of runs from file
 *
 * @param runs	vector into which to store list of runs
 * @param fnmae	text file to read from
 *
 * @note code sorts list of runs and removes duplicates when needed
 */
static void readRuns(std::vector<uint64_t>& runs, const std::string& fname)
{
    std::ifstream infile(fname);
    if (infile.bad() || infile.fail())
	throw std::runtime_error("unable to open run list file");
    // large enough that we most likely never need to realloc
    runs.reserve(1 << 18);
    bool needsSort = false;
    // read runs from file (minimal error handling)
    for (uint64_t run = 0, lastrun = 0; infile >> run; lastrun = run) {
	runs.push_back(run);
	// check for runs being in order
	needsSort |= run > lastrun;
    }
    if (infile.bad()) {
	throw std::runtime_error("reading from run list file");
    } else if (infile.eof()) {
	// all fine, end of file reached...
	if (needsSort) {
	    if (1 < runs.size()) std::sort(std::begin(runs), std::end(runs));
	    // make sure run numbers occur only once
	    auto it = std::unique(std::begin(runs), std::end(runs));
	    if (std::end(runs) != it) runs.erase(it, std::end(runs));
	}
	return;
    } else if (infile.fail()) {
	throw std::domain_error("unable to convert number in run list file");
    }
    return;
}

/** @brief write list of runs to file
 *
 * @param fname	destination file name
 * @param runs	list of runs
 *
 * @note: data is first written to temporary file, then the temp. file is
 * renamed to fname to make sure the update appears atomic to any process
 * reading from fname. (reading processes will either get the old version, or
 * the new one, but they should never see a corrupt or partially written file)
 */
static void writeRuns(const std::string& fname,
	const std::vector<uint64_t>& runs)
{
    std::string tempfname(fname + ".temp");
    {
	std::ofstream outfile(tempfname);
	for (uint64_t run: runs) outfile << run << std::endl;
	if (outfile.bad()) {
	    throw std::runtime_error("writing to run list file");
	} else if (outfile.fail()) {
	    throw std::logic_error("logic error while writing run list file");
	}
    }
    if (0 != std::rename(tempfname.c_str(), fname.c_str())) {
	throw std::system_error(errno, std::system_category(),
		"error renaming run list file");
    }
    return;
}

/** @brief display usage information */
static void help [[noreturn]] (const char* cmdname)
{
    std::cout << "usage:" << std::endl <<
	"\t" << cmdname << " [options] [run number(s)]" << std::endl <<
	std::endl <<
	"options:" << std::endl <<
	"-a, --add\t\tadd run numbers to run list file (default)" << std::endl <<
	"-f, --file [file]\trun list file to modify" << std::endl <<
	"-h, --help\t\tdisplay usage information" << std::endl <<
	"-r, --remove\t\tremove given run numbers from run list file" << std::endl;
    std::exit(0);
}

/** @brief crack options given on command line
 *
 * @param argc		argc from main
 * @param argv		argv from main
 * @param remove	set to true if options indicate runs are to be removed
 * @param fname		set to name of text file given on command line
 * @param runs		filled with list of runs to add/remove
 */
static void crackopt(int argc, char* const argv[],
	bool& remove, std::string& fname,
	std::vector<uint64_t>& runs)
{
    // options understood by program
    static const char* optstr = "af:hr";
    static const struct option longopts[] = {
	{ "add",    no_argument,       0, 'a' },
	{ "file",   required_argument, 0, 'f' },
	{ "help",   no_argument,       0, 'h' },
	{ "remove", no_argument,       0, 'r' },
	{ nullptr,  0,                 0, 0   }
    };

    // set defaults
    remove = false;
    fname = "";
    runs.clear();

    // make sure there's only one add/remove
    bool haveAddRemove = false;
    // process options
    for (int opt = getopt_long(argc, argv, optstr, longopts, nullptr);
	    -1 != opt;
	    opt = getopt_long(argc, argv, optstr, longopts, nullptr)) {
	switch (opt) {
	    case 'a':
	    case 'r':
		if (haveAddRemove)
		    throw std::logic_error(
			    "may only specify exactly one of --add/--remove");
		haveAddRemove = true;
		remove = ('r' == opt);
		break;
	    case 'f':
		if (!fname.empty() || 0 != fname.size())
		    throw std::logic_error(
			    "multiple run list files not allowed");
		fname = optarg;
		break;
	    case 'h':
		help(argv[0]);
		break;
	    case '?':
	    default:
		throw std::invalid_argument(
			"unknown option passed on command line");
	};
    }
    // reserve space for run numbers, and try to convert
    runs.reserve(argc - optind);
    for (; optind < argc; ++optind) {
	std::istringstream istr(argv[optind]);
	uint64_t run;
	if (!(istr >> run))
	    throw std::domain_error(
		    "unable to convert non-option argument to run number");
	runs.push_back(run);
    }
}

/// main routine of program
int main(int argc, char* const argv[])
{
    std::string fname;
    bool remove;
    std::vector<uint64_t> runs, runlist;

    try {
	crackopt(argc, argv, remove, fname, runs);
	if (fname.empty() || 0 == fname.size())
	    throw std::invalid_argument("run list file name cannot be empty.");
	// see if we have anything to do (empty list of runs to add/remove?)
	if (!runs.empty()) {
	    // try to acquire lock for fname - if we don't succees in 5
	    // minutes, the constructor will throw
	    DotLock lock(fname, 300);
	    readRuns(runlist, fname);
	    addRemoveRuns(runlist, runs, remove);
	    writeRuns(fname, runlist);
	} // lock release here
    } catch (const std::exception& e) {
	// make sure we dump some information to stderr, so we can learn what
	// went wrong from the log file
	const auto& t = typeid(e);
	char *demangled = nullptr;
	size_t demangledsz = 0;
	int status = 0;
	// demangle exception name (if possible)
	demangled = __cxxabiv1::__cxa_demangle(t.name(), demangled,
		&demangledsz, &status);
	std::cerr << "Caught exception of type " <<
	    ((0 == status) ? demangled : t.name()) << ":" <<
	    std::endl <<
	    "\t" << e.what() << std::endl;
	std::free(demangled);
	// signal failure
	return 1;
    }
    return 0;
}

// vim: sw=4:tw=78:ft=cpp
