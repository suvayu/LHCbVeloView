/** @file VersionedObject.h
 *
 * @author Manuel Schiller <manuel.schiller@nikhef.nl>
 * @date 2013-04-15
 */

#ifndef VERSIONED_OBJECT
#define VERSIONED_OBJECT

#include <vector>

#include "TimeStamp.h"

template <class T, class VEROBJ = TimeStamp> class VersionedObject
{
    public:
	typedef T value_type;
	typedef VEROBJ version_type;

    private:
	/// keep the version information around
	std::vector<version_type> m_vers;
	/// keep the objects around
	std::vector<value_type> m_objs;
};

#endif // VERSIONED_OBJECT

// vim: sw=4:tw=78:ft=c++
