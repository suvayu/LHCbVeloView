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
// instantiate templates most likely to be useful

// the following should not be needed because ROOT's type redefinition madness
// should already cover these
//template class VersionedObject<bool>;
//template class VersionedObject<char>;
//template class VersionedObject<unsigned char>;
//template class VersionedObject<short>;
//template class VersionedObject<unsigned short>;
//template class VersionedObject<int>;
//template class VersionedObject<unsigned int>;
//template class VersionedObject<long>;
//template class VersionedObject<unsigned long>;
//template class VersionedObject<long long>;
//template class VersionedObject<unsigned long long>;
//template class VersionedObject<float>;
//template class VersionedObject<double>;
//
//template class VersionedObject<std::vector<bool> >
//template class VersionedObject<std::vector<char> >;
//template class VersionedObject<std::vector<unsigned char> >;
//template class VersionedObject<std::vector<short> >;
//template class VersionedObject<std::vector<unsigned short> >;
//template class VersionedObject<std::vector<int> >;
//template class VersionedObject<std::vector<unsigned int> >;
//template class VersionedObject<std::vector<long> >;
//template class VersionedObject<std::vector<unsigned long> >;
//template class VersionedObject<std::vector<long long> >;
//template class VersionedObject<std::vector<unsigned long long> >;
//template class VersionedObject<std::vector<float> >;
//template class VersionedObject<std::vector<double> >;
//
//template class VersionedObject<std::map<int, bool> >;
//template class VersionedObject<std::map<int, char> >;
//template class VersionedObject<std::map<int, unsigned char> >;
//template class VersionedObject<std::map<int, short> >;
//template class VersionedObject<std::map<int, unsigned short> >;
//template class VersionedObject<std::map<int, int> >;
//template class VersionedObject<std::map<int, unsigned int> >;
//template class VersionedObject<std::map<int, long> >;
//template class VersionedObject<std::map<int, unsigned long> >;
//template class VersionedObject<std::map<int, long long> >;
//template class VersionedObject<std::map<int, unsigned long long> >;
//template class VersionedObject<std::map<int, float> >;
//template class VersionedObject<std::map<int, double> >;

template class VersionedObject<std::string>;

template class VersionedObject<Bool_t>;
template class VersionedObject<Char_t>;
template class VersionedObject<UChar_t>;
template class VersionedObject<Short_t>;
template class VersionedObject<UShort_t>;
template class VersionedObject<Int_t>;
template class VersionedObject<UInt_t>;
template class VersionedObject<Long_t>;
template class VersionedObject<ULong_t>;
template class VersionedObject<Long64_t>;
template class VersionedObject<ULong64_t>;
template class VersionedObject<Float_t>;
template class VersionedObject<Double_t>;
//template class VersionedObject<Float16_t>;
//template class VersionedObject<Double32_t>;

template class VersionedObject<std::vector<Char_t> >;
template class VersionedObject<std::vector<UChar_t> >;
template class VersionedObject<std::vector<Short_t> >;
template class VersionedObject<std::vector<UShort_t> >;
template class VersionedObject<std::vector<Int_t> >;
template class VersionedObject<std::vector<UInt_t> >;
template class VersionedObject<std::vector<Long_t> >;
template class VersionedObject<std::vector<ULong_t> >;
template class VersionedObject<std::vector<Long64_t> >;
template class VersionedObject<std::vector<ULong64_t> >;
template class VersionedObject<std::vector<Float_t> >;
template class VersionedObject<std::vector<Double_t> >;
//template class VersionedObject<std::vector<Float16_t> >;
//template class VersionedObject<std::vector<Double32_t> >;

template class VersionedObject<std::map<int, Char_t> >;
template class VersionedObject<std::map<int, UChar_t> >;
template class VersionedObject<std::map<int, Short_t> >;
template class VersionedObject<std::map<int, UShort_t> >;
template class VersionedObject<std::map<int, Int_t> >;
template class VersionedObject<std::map<int, UInt_t> >;
template class VersionedObject<std::map<int, Long_t> >;
template class VersionedObject<std::map<int, ULong_t> >;
template class VersionedObject<std::map<int, Long64_t> >;
template class VersionedObject<std::map<int, ULong64_t> >;
template class VersionedObject<std::map<int, Float_t> >;
template class VersionedObject<std::map<int, Double_t> >;
//template class VersionedObject<std::map<int, Float16_t> >;
//template class VersionedObject<std::map<int, Double32_t> >;
#else
#error "Never include VersionedObjectInstantiations.h directly."
#endif

#endif // VERSIONEDOBJECTINSTANTIATIONS_H

// vim: sw=4:tw=78:ft=cpp
