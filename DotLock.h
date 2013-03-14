/**
 * @file DotLock.h
 * @author Manuel Schiller
 * @date 2009-08-06
 */
#ifndef DOTLOCK_H
#define DOTLOCK_H

#include <string>
#include <exception>

/// class acquiring a dotlock while in existence
class DotLock
{
    public:
	/// constructor
	DotLock(const char* filename);
	/// constructor
	DotLock(const std::string& filename);
	/// destructor
	virtual ~DotLock();
    private:
	/// name of lock file
	std::string m_dotlockfilename;
	/// initialise
	void init();
	/// routine to acquire lock (returns errno, doesn't leak resources)
	int getlock(const char* fname) const;
	/// routine to release lock (returns errno, doesn't leak resources)
	static int releaselock(const char* fname);
	/// routine for safe reading/writing (returns errno, doesn't leak)
	static int xfer(const char* fname, bool read, std::size_t sz, char* buf);
	/// fully qualified host name (no leaks, if NULL, errno says why)
	static char* gethostname();
	/// xor val into arr
	static void xor_in(unsigned char (&arr)[8], unsigned long long val);

	/// throw a DotLockExpection in case of trouble during locking
	class DotLockException : public std::exception
        {
	    private:
		/// size of static buffer for error message from strerror_r
		static const int s_sz = 256;
		/// pointer to error from getaddrinfo
		const char* m_gaierr;
		/// need static buffer for error message from strerror_r
		char m_buf[s_sz];
	    public:
		/// constructor
		DotLockException(int err, bool isgetaddrinfoerr = false);
		/// routine returning a C string describing what went wrong
		const char* what() const throw ();
	};
};

#endif // DOTLOCK_H

// vim:tw=78:sw=4:ft=cpp
