/** @file VersionedObjectInstantiations.h
 *
 * @author Manuel Schiller <manuel.schiller@nikhef.nl>
 * @date 2013-04-15
 *
 * Never include this file directly
 */

#ifndef VERSIONEDOBJECTINSTANTIATIONS_H
#define VERSIONEDOBJECTINSTANTIATIONS_H

#ifdef INSTANTIATE_VERSIONEDOBJECTS_NOW
// get ROOT predefined types
#include <Rtypes.h>

// Instantiate templates most likely to be useful, those include all the basic
// types provided by the language (bool, char, short, ...)
//
// We'll need some machinery for that:
// - a macro helper macro which instantiates a class: INSTANTIATE
// - a macro to put a comma into a macro argument: COMMA (the preprocessor
//   uses a comma as argument separator, so it needs some form of protection
//   from the greedy preprocessor... ;)
// - a macro which does the instantiation for all the basic types:
//   INSTANTIATE_BASICTYPES
//
// The following code is not too readable, but it saves lots of typing
#undef COMMA
#undef INSTANTIATE
#undef INSTANTIATE_BASICTYPES
#define COMMA ,
#define INSTANTIATE(CLASS, ...) template class CLASS <__VA_ARGS__>;
#define INSTANTIATE_BASICTYPES(CLASS, PFX, SFX) \
    INSTANTIATE(CLASS, PFX Char_t SFX) \
    INSTANTIATE(CLASS, PFX UChar_t SFX) \
    INSTANTIATE(CLASS, PFX Short_t SFX) \
    INSTANTIATE(CLASS, PFX UShort_t SFX) \
    INSTANTIATE(CLASS, PFX Int_t SFX) \
    INSTANTIATE(CLASS, PFX UInt_t SFX) \
    INSTANTIATE(CLASS, PFX Long_t SFX) \
    INSTANTIATE(CLASS, PFX ULong_t SFX) \
    INSTANTIATE(CLASS, PFX Long64_t SFX) \
    INSTANTIATE(CLASS, PFX ULong64_t SFX) \
    INSTANTIATE(CLASS, PFX Float_t SFX) \
    INSTANTIATE(CLASS, PFX Double_t SFX) 
//    INSTANTIATE(CLASS, PFX Bool_t SFX)

////////////////////////////////////////////////////////////////////////
// instatiate VersionedObject
////////////////////////////////////////////////////////////////////////
// scalars
INSTANTIATE_BASICTYPES(VersionedObject, , )
// vectors
INSTANTIATE_BASICTYPES(VersionedObject, std::vector<, >)
// vectors of vectors (2D)
INSTANTIATE_BASICTYPES(VersionedObject, std::vector<std::vector<, > >)
// vectors of sparse vectors (2D)
INSTANTIATE_BASICTYPES(VersionedObject, std::vector<std::map<int COMMA, > >)
// sparse vectors
INSTANTIATE_BASICTYPES(VersionedObject, std::map<int COMMA, >)
// sparse vectors of vectors (2D)
INSTANTIATE_BASICTYPES(VersionedObject, std::map<int COMMA std::vector<, > >)
// sparse vectors of sparse vectors (2D)
INSTANTIATE_BASICTYPES(VersionedObject, std::map<int COMMA std::map<int COMMA, > >)

template class VersionedObject<std::string>;

////////////////////////////////////////////////////////////////////////
// instatiate underlying std::vectors
////////////////////////////////////////////////////////////////////////
INSTANTIATE_BASICTYPES(std::vector, , )
INSTANTIATE_BASICTYPES(std::vector, std::vector<, >)
INSTANTIATE_BASICTYPES(std::vector, std::map<int COMMA , >)

////////////////////////////////////////////////////////////////////////
// instatiate underlying std::maps
////////////////////////////////////////////////////////////////////////
INSTANTIATE_BASICTYPES(std::map, int COMMA, )
INSTANTIATE_BASICTYPES(std::map, int COMMA std::vector<, >)
INSTANTIATE_BASICTYPES(std::map, int COMMA std::map<int COMMA , >)

#undef COMMA
#undef INSTANTIATE
#undef INSTANTIATE_BASICTYPES
#else
#error "Never include VersionedObjectInstantiations.h directly."
#endif

#endif // VERSIONEDOBJECTINSTANTIATIONS_H

// vim: sw=4:tw=78:ft=cpp
