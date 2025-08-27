https://gramps-project.org/api_5_1_x/gen/gen_lib.html#gramps.gen.lib.primaryobj.PrimaryObject

# The [`gramps.gen.lib`](#module-gramps.gen.lib) Module[¶](#module-gramps.gen.lib)
The core library of Gramps objects

## Base objects[¶](#base-objects)

### BaseObject[¶](#module-gramps.gen.lib.baseobj)
Base Object class for Gramps

*class *`gramps.gen.lib.baseobj.``BaseObject`[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject)[¶](#gramps.gen.lib.baseobj.BaseObject)
Bases: `object`

The BaseObject is the base class for all data objects in Gramps,
whether primary or not.

Its main goal is to provide common capabilites to all objects, such as
searching through all available information.

*classmethod *`create`(*data*)[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.create)[¶](#gramps.gen.lib.baseobj.BaseObject.create)
Create a new instance from serialized data.

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.get_handle_referents)[¶](#gramps.gen.lib.baseobj.BaseObject.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.get_referenced_handles)[¶](#gramps.gen.lib.baseobj.BaseObject.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
Returns the list of (classname, handle) tuples for referenced
objects.

Return type
list

`get_referenced_handles_recursively`()[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.get_referenced_handles_recursively)[¶](#gramps.gen.lib.baseobj.BaseObject.get_referenced_handles_recursively)
Return the list of (classname, handle) tuples for all referenced
primary objects, whether directly or through child objects.

Returns
Returns the list of (classname, handle) tuples for referenced
objects.

Return type
list

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.get_text_data_child_list)[¶](#gramps.gen.lib.baseobj.BaseObject.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.get_text_data_list)[¶](#gramps.gen.lib.baseobj.BaseObject.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`matches_regexp`(*pattern*, *case_sensitive=False*)[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.matches_regexp)[¶](#gramps.gen.lib.baseobj.BaseObject.matches_regexp)
Return True if any text data in the object or any of it’s child
objects matches a given regular expression.

Parameters
**pattern** (*str*) – The pattern to match.

Returns
Returns whether any text data in the object or any of it’s
child objects matches a given regexp.

Return type
bool

`matches_string`(*pattern*, *case_sensitive=False*)[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.matches_string)[¶](#gramps.gen.lib.baseobj.BaseObject.matches_string)
Return True if any text data in the object or any of it’s child
objects matches a given pattern.

Parameters

- **pattern** (*str*) – The pattern to match.

- **case_sensitive** (*bool*) – Whether the match is case-sensitive.

Returns
Returns whether any text data in the object or any of it’s
child objects matches a given pattern.

Return type
bool

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.merge)[¶](#gramps.gen.lib.baseobj.BaseObject.merge)
Merge content of this object with that of acquisition.

There are two sides to merger. First, the content of acquisition needs
to be incorporated. Second, handles that reference acquisition (if
there are any) need to be updated. Only the first part is handled in
gen.lib, the second part needs access to the database and should be
done in its own routines.

Parameters
**acquisition** ([*BaseObject*](#gramps.gen.lib.baseobj.BaseObject)) – The object to incorporate.

`serialize`()[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.serialize)[¶](#gramps.gen.lib.baseobj.BaseObject.serialize)
Convert the object to a serialized tuple of data.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/baseobj.html#BaseObject.unserialize)[¶](#gramps.gen.lib.baseobj.BaseObject.unserialize)
Convert a serialized tuple of data to an object.

### AddressBase[¶](#module-gramps.gen.lib.addressbase)
AddressBase class for Gramps.

*class *`gramps.gen.lib.addressbase.``AddressBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/addressbase.html#AddressBase)[¶](#gramps.gen.lib.addressbase.AddressBase)
Bases: `object`

Base class for address-aware objects.

`add_address`(*address*)[[source]](../_modules/gramps/gen/lib/addressbase.html#AddressBase.add_address)[¶](#gramps.gen.lib.addressbase.AddressBase.add_address)
Add the [`Address`](#gramps.gen.lib.address.Address) instance to the object’s list of
addresses.

Parameters
**address** (*list*) – [`Address`](#gramps.gen.lib.address.Address) instance to add to the
object’s address list

`get_address_list`()[[source]](../_modules/gramps/gen/lib/addressbase.html#AddressBase.get_address_list)[¶](#gramps.gen.lib.addressbase.AddressBase.get_address_list)
Return the list of [`Address`](#gramps.gen.lib.address.Address) instances associated with
the object.

Returns
Returns the list of [`Address`](#gramps.gen.lib.address.Address) instances

Return type
list

`remove_address`(*address*)[[source]](../_modules/gramps/gen/lib/addressbase.html#AddressBase.remove_address)[¶](#gramps.gen.lib.addressbase.AddressBase.remove_address)
Remove the specified [`Address`](#gramps.gen.lib.address.Address) instance from the address list.

If the instance does not exist in the list, the operation has
no effect.

Parameters
**address** ([`Address`](#gramps.gen.lib.address.Address)) – [`Address`](#gramps.gen.lib.address.Address) instance to remove from the
list

Returns
True if the address was removed, False if it was not in the
list.

Return type
bool

`serialize`()[[source]](../_modules/gramps/gen/lib/addressbase.html#AddressBase.serialize)[¶](#gramps.gen.lib.addressbase.AddressBase.serialize)
Convert the object to a serialized tuple of data.

`set_address_list`(*address_list*)[[source]](../_modules/gramps/gen/lib/addressbase.html#AddressBase.set_address_list)[¶](#gramps.gen.lib.addressbase.AddressBase.set_address_list)
Assign the passed list to the object’s list of
[`Address`](#gramps.gen.lib.address.Address) instances.

Parameters
**address_list** (*list*) – List of [`Address`](#gramps.gen.lib.address.Address) instances to be
associated with the object

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/addressbase.html#AddressBase.unserialize)[¶](#gramps.gen.lib.addressbase.AddressBase.unserialize)
Convert a serialized tuple of data to an object.

### AttributeRootBase[¶](#module-gramps.gen.lib.attrbase)
AttributeRootBase class for Gramps.

*class *`gramps.gen.lib.attrbase.``AttributeRootBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/attrbase.html#AttributeRootBase)[¶](#gramps.gen.lib.attrbase.AttributeRootBase)
Bases: `object`

Base class for attribute-aware objects.

`add_attribute`(*attribute*)[[source]](../_modules/gramps/gen/lib/attrbase.html#AttributeRootBase.add_attribute)[¶](#gramps.gen.lib.attrbase.AttributeRootBase.add_attribute)
Add the [`Attribute`](#gramps.gen.lib.attribute.Attribute) instance to the object’s list of
attributes.

Parameters
**attribute** ([`Attribute`](#gramps.gen.lib.attribute.Attribute)) – [`Attribute`](#gramps.gen.lib.attribute.Attribute) instance to add.

`get_attribute_list`()[[source]](../_modules/gramps/gen/lib/attrbase.html#AttributeRootBase.get_attribute_list)[¶](#gramps.gen.lib.attrbase.AttributeRootBase.get_attribute_list)
Return the list of [`Attribute`](#gramps.gen.lib.attribute.Attribute) instances associated
with the object.

Returns
Returns the list of [`Attribute`](#gramps.gen.lib.attribute.Attribute) instances.

Return type
list

`remove_attribute`(*attribute*)[[source]](../_modules/gramps/gen/lib/attrbase.html#AttributeRootBase.remove_attribute)[¶](#gramps.gen.lib.attrbase.AttributeRootBase.remove_attribute)
Remove the specified [`Attribute`](#gramps.gen.lib.attribute.Attribute) instance from the
attribute list.

If the instance does not exist in the list, the operation has
no effect.

Parameters
**attribute** ([`Attribute`](#gramps.gen.lib.attribute.Attribute)) – [`Attribute`](#gramps.gen.lib.attribute.Attribute) instance to remove
from the list

Returns
True if the attribute was removed, False if it was not in the
list.

Return type
bool

`serialize`()[[source]](../_modules/gramps/gen/lib/attrbase.html#AttributeRootBase.serialize)[¶](#gramps.gen.lib.attrbase.AttributeRootBase.serialize)
Convert the object to a serialized tuple of data.

`set_attribute_list`(*attribute_list*)[[source]](../_modules/gramps/gen/lib/attrbase.html#AttributeRootBase.set_attribute_list)[¶](#gramps.gen.lib.attrbase.AttributeRootBase.set_attribute_list)
Assign the passed list to the Person’s list of
[`Attribute`](#gramps.gen.lib.attribute.Attribute) instances.

Parameters
**attribute_list** (*list*) – List of [`Attribute`](#gramps.gen.lib.attribute.Attribute) instances
to ba associated with the Person

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/attrbase.html#AttributeRootBase.unserialize)[¶](#gramps.gen.lib.attrbase.AttributeRootBase.unserialize)
Convert a serialized tuple of data to an object.

### AttributeBase[¶](#attributebase)

*class *`gramps.gen.lib.attrbase.``AttributeBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/attrbase.html#AttributeBase)[¶](#gramps.gen.lib.attrbase.AttributeBase)
Bases: [`gramps.gen.lib.attrbase.AttributeRootBase`](#gramps.gen.lib.attrbase.AttributeRootBase)

### SrcAttributeBase[¶](#srcattributebase)

*class *`gramps.gen.lib.attrbase.``SrcAttributeBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/attrbase.html#SrcAttributeBase)[¶](#gramps.gen.lib.attrbase.SrcAttributeBase)
Bases: [`gramps.gen.lib.attrbase.AttributeRootBase`](#gramps.gen.lib.attrbase.AttributeRootBase)

### CitationBase[¶](#module-gramps.gen.lib.citationbase)
CitationBase class for Gramps.

*class *`gramps.gen.lib.citationbase.``CitationBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase)[¶](#gramps.gen.lib.citationbase.CitationBase)
Bases: `object`

Base class for storing citations.

Starting in 3.4, the objects may have multiple citations.
Internally, this class maintains a list of Citation handles,
as a citation_list attribute of the CitationBase object.
This class is analogous to the notebase class.
Both these have no attributes of their own; in this respect, they differ
from classes like MediaRef, which does have attributes (in that case,
privacy, sources, notes and attributes).

This class, together with the Citation class, replaces the old SourceRef
class. I.e. SourceRef = CitationBase + Citation

`add_citation`(*handle*)[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.add_citation)[¶](#gramps.gen.lib.citationbase.CitationBase.add_citation)
Add the [`Citation`](#gramps.gen.lib.citation.Citation) handle to the list of citation
handles.

Parameters
**handle** (*str*) – [`Citation`](#gramps.gen.lib.citation.Citation) handle to add the list of
citations

Returns
True if handle was added, False if it already was in the list

Return type
bool

`get_all_citation_lists`()[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.get_all_citation_lists)[¶](#gramps.gen.lib.citationbase.CitationBase.get_all_citation_lists)
Return the list of [`Citation`](#gramps.gen.lib.citation.Citation) handles associated with
the object or with child objects.

Returns
The list of [`Citation`](#gramps.gen.lib.citation.Citation) handles

Return type
list

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.get_citation_child_list)[¶](#gramps.gen.lib.citationbase.CitationBase.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

All methods which inherit from CitationBase and have other child objects
with citations, should return here a list of child objects which are
CitationBase

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_citation_list`()[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.get_citation_list)[¶](#gramps.gen.lib.citationbase.CitationBase.get_citation_list)
Return the list of [`Citation`](#gramps.gen.lib.citation.Citation) handles associated with
the object.

Returns
The list of [`Citation`](#gramps.gen.lib.citation.Citation) handles

Return type
list

`get_referenced_citation_handles`()[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.get_referenced_citation_handles)[¶](#gramps.gen.lib.citationbase.CitationBase.get_referenced_citation_handles)
Return the list of (classname, handle) tuples for all referenced
citations.

This method should be used to get the [`Citation`](#gramps.gen.lib.citation.Citation)
portion of the list by objects that store citation lists.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

`has_citation_reference`(*citation_handle*)[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.has_citation_reference)[¶](#gramps.gen.lib.citationbase.CitationBase.has_citation_reference)
Return True if the object or any of its child objects has reference
to this citation handle.

Parameters
**citation_handle** (*str*) – The citation handle to be checked.

Returns
Returns whether the object or any of its child objects has
reference to this citation handle.

Return type
bool

`remove_citation_references`(*citation_handle_list*)[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.remove_citation_references)[¶](#gramps.gen.lib.citationbase.CitationBase.remove_citation_references)
Remove the specified handles from the list of citation handles, and all
secondary child objects.

Parameters
**citation_handle_list** – The list of citation handles to be removed

`replace_citation_references`(*old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.replace_citation_references)[¶](#gramps.gen.lib.citationbase.CitationBase.replace_citation_references)
Replace references to citation handles in the list of this object and
all child objects and merge equivalent entries.

Parameters

- **old_handle** (*str*) – The citation handle to be replaced.

- **new_handle** (*str*) – The citation handle to replace the old one with.

`serialize`()[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.serialize)[¶](#gramps.gen.lib.citationbase.CitationBase.serialize)
Convert the object to a serialized tuple of data.

`set_citation_list`(*citation_list*)[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.set_citation_list)[¶](#gramps.gen.lib.citationbase.CitationBase.set_citation_list)
Assign the passed list to be object’s list of
[`Citation`](#gramps.gen.lib.citation.Citation) handles.

Parameters
**citation_list** (*list*) – List of [`Citation`](#gramps.gen.lib.citation.Citation) handles to
be set on the object

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/citationbase.html#CitationBase.unserialize)[¶](#gramps.gen.lib.citationbase.CitationBase.unserialize)
Convert a serialized tuple of data to an object.

### IndirectCitationBase[¶](#indirectcitationbase)

*class *`gramps.gen.lib.citationbase.``IndirectCitationBase`[[source]](../_modules/gramps/gen/lib/citationbase.html#IndirectCitationBase)[¶](#gramps.gen.lib.citationbase.IndirectCitationBase)
Bases: `object`

Citation management logic for objects that don’t have citations
for the primary objects, but only for the child (secondary) ones.

The derived class must implement the
[`get_citation_child_list()`](#gramps.gen.lib.citationbase.CitationBase.get_citation_child_list) method to return the list of
child secondary objects that may refer citations.

Note

for most objects, this functionality is inherited from
[`CitationBase`](#gramps.gen.lib.citationbase.CitationBase), which checks both the object and the child
objects.

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/citationbase.html#IndirectCitationBase.get_citation_child_list)[¶](#gramps.gen.lib.citationbase.IndirectCitationBase.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

All methods which inherit from CitationBase and have other child objects
with citations, should return here a list of child objects which are
CitationBase

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_citation_list`()[[source]](../_modules/gramps/gen/lib/citationbase.html#IndirectCitationBase.get_citation_list)[¶](#gramps.gen.lib.citationbase.IndirectCitationBase.get_citation_list)
Return the list of `Citation` handles
associated with the object. For an IndirectCitationBase this is always
the empty list
:returns: The list of `Citation` handles
:rtype: list

`has_citation_reference`(*citation_handle*)[[source]](../_modules/gramps/gen/lib/citationbase.html#IndirectCitationBase.has_citation_reference)[¶](#gramps.gen.lib.citationbase.IndirectCitationBase.has_citation_reference)
Return True if any of the child objects has reference to this citation
handle.

Parameters
**citation_handle** (*str*) – The citation handle to be checked.

Returns
Returns whether any of it’s child objects has reference to
this citation handle.

Return type
bool

`remove_citation_references`(*citation_handle_list*)[[source]](../_modules/gramps/gen/lib/citationbase.html#IndirectCitationBase.remove_citation_references)[¶](#gramps.gen.lib.citationbase.IndirectCitationBase.remove_citation_references)
Remove references to all citation handles in the list in all child
objects.

Parameters
**citation_handle_list** (*list*) – The list of citation handles to be removed.

`replace_citation_references`(*old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/citationbase.html#IndirectCitationBase.replace_citation_references)[¶](#gramps.gen.lib.citationbase.IndirectCitationBase.replace_citation_references)
Replace references to citation handles in all child objects and merge
equivalent entries.

Parameters

- **old_handle** (*str*) – The citation handle to be replaced.

- **new_handle** (*str*) – The citation handle to replace the old one with.

### DateBase[¶](#module-gramps.gen.lib.datebase)
DateBase class for Gramps.

*class *`gramps.gen.lib.datebase.``DateBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/datebase.html#DateBase)[¶](#gramps.gen.lib.datebase.DateBase)
Bases: `object`

Base class for storing date information.

`get_date_object`()[[source]](../_modules/gramps/gen/lib/datebase.html#DateBase.get_date_object)[¶](#gramps.gen.lib.datebase.DateBase.get_date_object)
Return the [`Date`](#gramps.gen.lib.date.Date) object associated with the DateBase.

Returns
Returns a DateBase [`Date`](#gramps.gen.lib.date.Date) instance.

Return type
[`Date`](#gramps.gen.lib.date.Date)

`serialize`(*no_text_date=False*)[[source]](../_modules/gramps/gen/lib/datebase.html#DateBase.serialize)[¶](#gramps.gen.lib.datebase.DateBase.serialize)
Convert the object to a serialized tuple of data.

`set_date_object`(*date*)[[source]](../_modules/gramps/gen/lib/datebase.html#DateBase.set_date_object)[¶](#gramps.gen.lib.datebase.DateBase.set_date_object)
Set the [`Date`](#gramps.gen.lib.date.Date) object associated with the DateBase.

Parameters
**date** ([`Date`](#gramps.gen.lib.date.Date)) – [`Date`](#gramps.gen.lib.date.Date) instance to be assigned to the
DateBase

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/datebase.html#DateBase.unserialize)[¶](#gramps.gen.lib.datebase.DateBase.unserialize)
Convert a serialized tuple of data to an object.

### LdsOrdBase[¶](#module-gramps.gen.lib.ldsordbase)
LdsOrdBase class for Gramps.

*class *`gramps.gen.lib.ldsordbase.``LdsOrdBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/ldsordbase.html#LdsOrdBase)[¶](#gramps.gen.lib.ldsordbase.LdsOrdBase)
Bases: `object`

Base class for lds_ord-aware objects.

`add_lds_ord`(*lds_ord*)[[source]](../_modules/gramps/gen/lib/ldsordbase.html#LdsOrdBase.add_lds_ord)[¶](#gramps.gen.lib.ldsordbase.LdsOrdBase.add_lds_ord)
Add the [`LdsOrd`](#gramps.gen.lib.ldsord.LdsOrd) instance to the object’s list of
lds_ords.

Parameters
**lds_ord** (*list*) – [`LdsOrd`](#gramps.gen.lib.ldsord.LdsOrd) instance to add to the object’s
lds_ord list

`get_lds_ord_list`()[[source]](../_modules/gramps/gen/lib/ldsordbase.html#LdsOrdBase.get_lds_ord_list)[¶](#gramps.gen.lib.ldsordbase.LdsOrdBase.get_lds_ord_list)
Return the list of [`LdsOrd`](#gramps.gen.lib.ldsord.LdsOrd) instances associated with
the object.

Returns
Returns the list of [`LdsOrd`](#gramps.gen.lib.ldsord.LdsOrd) instances

Return type
list

`remove_lds_ord`(*lds_ord*)[[source]](../_modules/gramps/gen/lib/ldsordbase.html#LdsOrdBase.remove_lds_ord)[¶](#gramps.gen.lib.ldsordbase.LdsOrdBase.remove_lds_ord)
Remove the specified [`LdsOrd`](#gramps.gen.lib.ldsord.LdsOrd) instance from the lds_ord
list.

If the instance does not exist in the list, the operation has no effect.

Parameters
**lds_ord** ([`LdsOrd`](#gramps.gen.lib.ldsord.LdsOrd)) – [`LdsOrd`](#gramps.gen.lib.ldsord.LdsOrd) instance to remove from the
list

Returns
True if the lds_ord was removed, False if it was not in the
list.

Return type
bool

`serialize`()[[source]](../_modules/gramps/gen/lib/ldsordbase.html#LdsOrdBase.serialize)[¶](#gramps.gen.lib.ldsordbase.LdsOrdBase.serialize)
Convert the object to a serialized tuple of data.

`set_lds_ord_list`(*lds_ord_list*)[[source]](../_modules/gramps/gen/lib/ldsordbase.html#LdsOrdBase.set_lds_ord_list)[¶](#gramps.gen.lib.ldsordbase.LdsOrdBase.set_lds_ord_list)
Assign the passed list to the object’s list of [`LdsOrd`](#gramps.gen.lib.ldsord.LdsOrd)
instances.

Parameters
**lds_ord_list** (*list*) – List of [`LdsOrd`](#gramps.gen.lib.ldsord.LdsOrd) instances to be
associated with the object

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/ldsordbase.html#LdsOrdBase.unserialize)[¶](#gramps.gen.lib.ldsordbase.LdsOrdBase.unserialize)
Convert a serialized tuple of data to an object

### LocationBase[¶](#module-gramps.gen.lib.locationbase)
LocationBase class for Gramps.

*class *`gramps.gen.lib.locationbase.``LocationBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase)[¶](#gramps.gen.lib.locationbase.LocationBase)
Bases: `object`

Base class for all things Address.

`get_city`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.get_city)[¶](#gramps.gen.lib.locationbase.LocationBase.get_city)
Return the city name of the LocationBase object.

`get_country`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.get_country)[¶](#gramps.gen.lib.locationbase.LocationBase.get_country)
Return the country name of the LocationBase object.

`get_county`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.get_county)[¶](#gramps.gen.lib.locationbase.LocationBase.get_county)
Return the county name of the LocationBase object.

`get_locality`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.get_locality)[¶](#gramps.gen.lib.locationbase.LocationBase.get_locality)
Return the locality portion of the Location.

`get_phone`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.get_phone)[¶](#gramps.gen.lib.locationbase.LocationBase.get_phone)
Return the phone number of the LocationBase object.

`get_postal_code`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.get_postal_code)[¶](#gramps.gen.lib.locationbase.LocationBase.get_postal_code)
Return the postal code of the LocationBase object.

`get_state`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.get_state)[¶](#gramps.gen.lib.locationbase.LocationBase.get_state)
Return the state name of the LocationBase object.

`get_street`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.get_street)[¶](#gramps.gen.lib.locationbase.LocationBase.get_street)
Return the street portion of the Location.

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.get_text_data_list)[¶](#gramps.gen.lib.locationbase.LocationBase.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`serialize`()[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.serialize)[¶](#gramps.gen.lib.locationbase.LocationBase.serialize)
Convert the object to a serialized tuple of data.

`set_city`(*data*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.set_city)[¶](#gramps.gen.lib.locationbase.LocationBase.set_city)
Set the city name of the LocationBase object.

`set_country`(*data*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.set_country)[¶](#gramps.gen.lib.locationbase.LocationBase.set_country)
Set the country name of the LocationBase object.

`set_county`(*data*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.set_county)[¶](#gramps.gen.lib.locationbase.LocationBase.set_county)
Set the county name of the LocationBase object.

`set_locality`(*val*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.set_locality)[¶](#gramps.gen.lib.locationbase.LocationBase.set_locality)
Set the locality portion of the Location.

`set_phone`(*data*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.set_phone)[¶](#gramps.gen.lib.locationbase.LocationBase.set_phone)
Set the phone number of the LocationBase object.

`set_postal_code`(*data*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.set_postal_code)[¶](#gramps.gen.lib.locationbase.LocationBase.set_postal_code)
Set the postal code of the LocationBase object.

`set_state`(*data*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.set_state)[¶](#gramps.gen.lib.locationbase.LocationBase.set_state)
Set the state name of the LocationBase object.

`set_street`(*val*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.set_street)[¶](#gramps.gen.lib.locationbase.LocationBase.set_street)
Set the street portion of the Location.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/locationbase.html#LocationBase.unserialize)[¶](#gramps.gen.lib.locationbase.LocationBase.unserialize)
Convert a serialized tuple of data to an object.

### MediaBase[¶](#module-gramps.gen.lib.mediabase)
MediaBase class for Gramps.

*class *`gramps.gen.lib.mediabase.``MediaBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/mediabase.html#MediaBase)[¶](#gramps.gen.lib.mediabase.MediaBase)
Bases: `object`

Base class for storing media references.

`add_media_reference`(*media_ref*)[[source]](../_modules/gramps/gen/lib/mediabase.html#MediaBase.add_media_reference)[¶](#gramps.gen.lib.mediabase.MediaBase.add_media_reference)
Add a [`MediaRef`](#gramps.gen.lib.mediaref.MediaRef) instance to the object’s media list.

Parameters
**media_ref** ([`MediaRef`](#gramps.gen.lib.mediaref.MediaRef)) – [`MediaRef`](#gramps.gen.lib.mediaref.MediaRef) instance to be added to
the object’s media list.

`get_media_list`()[[source]](../_modules/gramps/gen/lib/mediabase.html#MediaBase.get_media_list)[¶](#gramps.gen.lib.mediabase.MediaBase.get_media_list)
Return the list of [`MediaRef`](#gramps.gen.lib.mediaref.MediaRef) instances associated
with the object.

Returns
list of [`MediaRef`](#gramps.gen.lib.mediaref.MediaRef) instances associated
with the object

Return type
list

`has_media_reference`(*obj_handle*)[[source]](../_modules/gramps/gen/lib/mediabase.html#MediaBase.has_media_reference)[¶](#gramps.gen.lib.mediabase.MediaBase.has_media_reference)
Return True if the object or any of it’s child objects has reference
to this media object handle.

Parameters
**obj_handle** (*str*) – The media handle to be checked.

Returns
Returns whether the object or any of it’s child objects has
reference to this media handle.

Return type
bool

`remove_media_references`(*obj_handle_list*)[[source]](../_modules/gramps/gen/lib/mediabase.html#MediaBase.remove_media_references)[¶](#gramps.gen.lib.mediabase.MediaBase.remove_media_references)
Remove references to all media handles in the list.

Parameters
**obj_handle_list** (*list*) – The list of media handles to be removed.

`replace_media_references`(*old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/mediabase.html#MediaBase.replace_media_references)[¶](#gramps.gen.lib.mediabase.MediaBase.replace_media_references)
Replace all references to old media handle with the new handle and
merge equivalent entries.

Parameters

- **old_handle** (*str*) – The media handle to be replaced.

- **new_handle** (*str*) – The media handle to replace the old one with.

`serialize`()[[source]](../_modules/gramps/gen/lib/mediabase.html#MediaBase.serialize)[¶](#gramps.gen.lib.mediabase.MediaBase.serialize)
Convert the object to a serialized tuple of data.

`set_media_list`(*media_ref_list*)[[source]](../_modules/gramps/gen/lib/mediabase.html#MediaBase.set_media_list)[¶](#gramps.gen.lib.mediabase.MediaBase.set_media_list)
Set the list of [`MediaRef`](#gramps.gen.lib.mediaref.MediaRef) instances associated with
the object. It replaces the previous list.

Parameters
**media_ref_list** (*list*) – list of [`MediaRef`](#gramps.gen.lib.mediaref.MediaRef) instances
to be assigned to the object.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/mediabase.html#MediaBase.unserialize)[¶](#gramps.gen.lib.mediabase.MediaBase.unserialize)
Convert a serialized tuple of data to an object.

### NoteBase[¶](#module-gramps.gen.lib.notebase)
NoteBase class for Gramps.

*class *`gramps.gen.lib.notebase.``NoteBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase)[¶](#gramps.gen.lib.notebase.NoteBase)
Bases: `object`

Base class for storing notes.

Starting in 3.0 branch, the objects may have multiple notes.
Internally, this class maintains a list of Note handles,
as a note_list attribute of the NoteBase object.

`add_note`(*handle*)[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.add_note)[¶](#gramps.gen.lib.notebase.NoteBase.add_note)
Add the [`Note`](#gramps.gen.lib.note.Note) handle to the list of note handles.

Parameters
**handle** (*str*) – [`Note`](#gramps.gen.lib.note.Note) handle to add the list of notes

Returns
True if handle was added, False if it already was in the list

Return type
bool

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.get_note_child_list)[¶](#gramps.gen.lib.notebase.NoteBase.get_note_child_list)
Return the list of child secondary objects that may refer notes.

All methods which inherit from NoteBase and have other child objects
with notes, should return here a list of child objects which are
NoteBase

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_note_list`()[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.get_note_list)[¶](#gramps.gen.lib.notebase.NoteBase.get_note_list)
Return the list of [`Note`](#gramps.gen.lib.note.Note) handles associated with the
object.

Returns
The list of [`Note`](#gramps.gen.lib.note.Note) handles

Return type
list

`get_referenced_note_handles`()[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.get_referenced_note_handles)[¶](#gramps.gen.lib.notebase.NoteBase.get_referenced_note_handles)
Return the list of (classname, handle) tuples for all referenced notes.

This method should be used to get the [`Note`](#gramps.gen.lib.note.Note) portion of
the list by objects that store note lists.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

`has_note_reference`(*note_handle*)[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.has_note_reference)[¶](#gramps.gen.lib.notebase.NoteBase.has_note_reference)
Return True if the object or any of its child objects has reference
to this note handle.

Parameters
**note_handle** (*str*) – The note handle to be checked.

Returns
Returns whether the object or any of its child objects has
reference to this note handle.

Return type
bool

`remove_note`(*handle*)[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.remove_note)[¶](#gramps.gen.lib.notebase.NoteBase.remove_note)
Remove the specified handle from the list of note handles, and all
secondary child objects.

Parameters
**handle** (*str*) – [`Note`](#gramps.gen.lib.note.Note) handle to remove from the list of
notes

`replace_note_references`(*old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.replace_note_references)[¶](#gramps.gen.lib.notebase.NoteBase.replace_note_references)
Replace references to note handles in the list of this object and
all child objects and merge equivalent entries.

Parameters

- **old_handle** (*str*) – The note handle to be replaced.

- **new_handle** (*str*) – The note handle to replace the old one with.

`serialize`()[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.serialize)[¶](#gramps.gen.lib.notebase.NoteBase.serialize)
Convert the object to a serialized tuple of data.

`set_note_list`(*note_list*)[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.set_note_list)[¶](#gramps.gen.lib.notebase.NoteBase.set_note_list)
Assign the passed list to be object’s list of [`Note`](#gramps.gen.lib.note.Note)
handles.

Parameters
**note_list** (*list*) – List of [`Note`](#gramps.gen.lib.note.Note) handles to be set on the
object

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/notebase.html#NoteBase.unserialize)[¶](#gramps.gen.lib.notebase.NoteBase.unserialize)
Convert a serialized tuple of data to an object.

### PlaceBase[¶](#module-gramps.gen.lib.placebase)
PlaceBase class for Gramps.

*class *`gramps.gen.lib.placebase.``PlaceBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/placebase.html#PlaceBase)[¶](#gramps.gen.lib.placebase.PlaceBase)
Bases: `object`

Base class for place-aware objects.

`get_place_handle`()[[source]](../_modules/gramps/gen/lib/placebase.html#PlaceBase.get_place_handle)[¶](#gramps.gen.lib.placebase.PlaceBase.get_place_handle)
Return the database handle of the [`Place`](#gramps.gen.lib.place.Place) associated
with the [`Event`](#gramps.gen.lib.event.Event).

Returns
[`Place`](#gramps.gen.lib.place.Place) database handle

Return type
str

`set_place_handle`(*place_handle*)[[source]](../_modules/gramps/gen/lib/placebase.html#PlaceBase.set_place_handle)[¶](#gramps.gen.lib.placebase.PlaceBase.set_place_handle)
Set the database handle for [`Place`](#gramps.gen.lib.place.Place) associated with the
object.

Parameters
**place_handle** (*str*) – [`Place`](#gramps.gen.lib.place.Place) database handle

### PrivacyBase[¶](#module-gramps.gen.lib.privacybase)
PrivacyBase Object class for Gramps.

*class *`gramps.gen.lib.privacybase.``PrivacyBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/privacybase.html#PrivacyBase)[¶](#gramps.gen.lib.privacybase.PrivacyBase)
Bases: `object`

Base class for privacy-aware objects.

`get_privacy`()[[source]](../_modules/gramps/gen/lib/privacybase.html#PrivacyBase.get_privacy)[¶](#gramps.gen.lib.privacybase.PrivacyBase.get_privacy)
Return the privacy level of the data.

Returns
True indicates that the record is private

Return type
bool

`serialize`()[[source]](../_modules/gramps/gen/lib/privacybase.html#PrivacyBase.serialize)[¶](#gramps.gen.lib.privacybase.PrivacyBase.serialize)
Convert the object to a serialized tuple of data.

`set_privacy`(*val*)[[source]](../_modules/gramps/gen/lib/privacybase.html#PrivacyBase.set_privacy)[¶](#gramps.gen.lib.privacybase.PrivacyBase.set_privacy)
Set or clears the privacy flag of the data.

Parameters
**val** (*bool*) – value to assign to the privacy flag. True indicates that
the record is private, False indicates that it is public.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/privacybase.html#PrivacyBase.unserialize)[¶](#gramps.gen.lib.privacybase.PrivacyBase.unserialize)
Convert a serialized tuple of data to an object.

### RefBase[¶](#module-gramps.gen.lib.refbase)
Base Reference class for Gramps.

*class *`gramps.gen.lib.refbase.``RefBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/refbase.html#RefBase)[¶](#gramps.gen.lib.refbase.RefBase)
Bases: `object`

Base reference class to manage references to other objects.

Any *Ref* classes should derive from this class.

`get_reference_handle`()[[source]](../_modules/gramps/gen/lib/refbase.html#RefBase.get_reference_handle)[¶](#gramps.gen.lib.refbase.RefBase.get_reference_handle)
Return the reference handle.

Returns
The reference handle.

Return type
str

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/refbase.html#RefBase.get_referenced_handles)[¶](#gramps.gen.lib.refbase.RefBase.get_referenced_handles)
Returns the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
Returns the list of (classname, handle) tuples for referenced
objects.

Return type
list

`serialize`()[[source]](../_modules/gramps/gen/lib/refbase.html#RefBase.serialize)[¶](#gramps.gen.lib.refbase.RefBase.serialize)
Convert the object to a serialized tuple of data.

`set_reference_handle`(*handle*)[[source]](../_modules/gramps/gen/lib/refbase.html#RefBase.set_reference_handle)[¶](#gramps.gen.lib.refbase.RefBase.set_reference_handle)
Set the reference handle.

Parameters
**handle** (*str*) – The reference handle.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/refbase.html#RefBase.unserialize)[¶](#gramps.gen.lib.refbase.RefBase.unserialize)
Convert a serialized tuple of data to an object.

### SurnameBase[¶](#module-gramps.gen.lib.surnamebase)
SurnameBase class for Gramps.

*class *`gramps.gen.lib.surnamebase.``SurnameBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase)[¶](#gramps.gen.lib.surnamebase.SurnameBase)
Bases: `object`

Base class for surname-aware objects.

`add_surname`(*surname*)[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.add_surname)[¶](#gramps.gen.lib.surnamebase.SurnameBase.add_surname)
Add the [`Surname`](#gramps.gen.lib.surname.Surname) instance to the object’s
list of surnames.

Parameters
**surname** – [`Surname`](#gramps.gen.lib.surname.Surname) instance to add to the
object’s address list.

`get_connectors`()[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.get_connectors)[¶](#gramps.gen.lib.surnamebase.SurnameBase.get_connectors)
Return a list of surnames (no prefix or connectors)

`get_prefixes`()[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.get_prefixes)[¶](#gramps.gen.lib.surnamebase.SurnameBase.get_prefixes)
Return a list of prefixes

`get_primary_surname`()[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.get_primary_surname)[¶](#gramps.gen.lib.surnamebase.SurnameBase.get_primary_surname)
Return the surname that is the primary surname

Returns
Returns the surname instance that is the primary surname. If
primary not set, and there is a surname, the first surname is
given, if no surnames, None is returned

Return type
[`Surname`](#gramps.gen.lib.surname.Surname) or None

`get_surname`()[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.get_surname)[¶](#gramps.gen.lib.surnamebase.SurnameBase.get_surname)
Return a fully formatted surname utilizing the surname_list

`get_surname_list`()[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.get_surname_list)[¶](#gramps.gen.lib.surnamebase.SurnameBase.get_surname_list)
Return the list of [`Surname`](#gramps.gen.lib.surname.Surname) instances
associated with the object.

Returns
Returns the list of [`Surname`](#gramps.gen.lib.surname.Surname) instances

Return type
list

`get_surnames`()[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.get_surnames)[¶](#gramps.gen.lib.surnamebase.SurnameBase.get_surnames)
Return a list of surnames (no prefix or connectors)

`get_upper_surname`()[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.get_upper_surname)[¶](#gramps.gen.lib.surnamebase.SurnameBase.get_upper_surname)
Return a fully formatted surname capitalized

`remove_surname`(*surname*)[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.remove_surname)[¶](#gramps.gen.lib.surnamebase.SurnameBase.remove_surname)
Remove the specified [`Surname`](#gramps.gen.lib.surname.Surname) instance from the
surname list.

If the instance does not exist in the list, the operation has
no effect.

Parameters
**surname** ([`Surname`](#gramps.gen.lib.surname.Surname)) – [`Surname`](#gramps.gen.lib.surname.Surname) instance to remove
from the list

Returns
True if the surname was removed, False if it was not in the
list.

Return type
bool

`serialize`()[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.serialize)[¶](#gramps.gen.lib.surnamebase.SurnameBase.serialize)
Convert the object to a serialized tuple of data.

`set_primary_surname`(*surnamenr=0*)[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.set_primary_surname)[¶](#gramps.gen.lib.surnamebase.SurnameBase.set_primary_surname)
Set the surname with surnamenr in the surname list as primary surname
Counting starts at 0

`set_surname_list`(*surname_list*)[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.set_surname_list)[¶](#gramps.gen.lib.surnamebase.SurnameBase.set_surname_list)
Assign the passed list to the object’s list of
[`Surname`](#gramps.gen.lib.surname.Surname) instances.

Parameters
**surname_list** (*list*) – List of [`Surname`](#gramps.gen.lib.surname.Surname) instances to be
associated with the object

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/surnamebase.html#SurnameBase.unserialize)[¶](#gramps.gen.lib.surnamebase.SurnameBase.unserialize)
Convert a serialized tuple of data to an object.

### TagBase[¶](#module-gramps.gen.lib.tagbase)
TagBase class for Gramps.

*class *`gramps.gen.lib.tagbase.``TagBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/tagbase.html#TagBase)[¶](#gramps.gen.lib.tagbase.TagBase)
Bases: `object`

Base class for tag-aware objects.

`add_tag`(*tag*)[[source]](../_modules/gramps/gen/lib/tagbase.html#TagBase.add_tag)[¶](#gramps.gen.lib.tagbase.TagBase.add_tag)
Add the tag to the object’s list of tags.

Parameters
**tag** (*unicode*) – unicode tag to add.

`get_referenced_tag_handles`()[[source]](../_modules/gramps/gen/lib/tagbase.html#TagBase.get_referenced_tag_handles)[¶](#gramps.gen.lib.tagbase.TagBase.get_referenced_tag_handles)
Return the list of (classname, handle) tuples for all referenced tags.

This method should be used to get the [`Tag`](#gramps.gen.lib.tag.Tag) portion
of the list by objects that store tag lists.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

`get_tag_list`()[[source]](../_modules/gramps/gen/lib/tagbase.html#TagBase.get_tag_list)[¶](#gramps.gen.lib.tagbase.TagBase.get_tag_list)
Return the list of tags associated with the object.

Returns
Returns the list of tags.

Return type
list

`remove_tag`(*tag*)[[source]](../_modules/gramps/gen/lib/tagbase.html#TagBase.remove_tag)[¶](#gramps.gen.lib.tagbase.TagBase.remove_tag)
Remove the specified tag from the tag list.

If the tag does not exist in the list, the operation has no effect.

Parameters
**tag** (*unicode*) – tag to remove from the list.

Returns
True if the tag was removed, False if it was not in the list.

Return type
bool

`replace_tag_references`(*old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/tagbase.html#TagBase.replace_tag_references)[¶](#gramps.gen.lib.tagbase.TagBase.replace_tag_references)
Replace references to note handles in the list of this object and
merge equivalent entries.

Parameters

- **old_handle** (*str*) – The note handle to be replaced.

- **new_handle** (*str*) – The note handle to replace the old one with.

`serialize`()[[source]](../_modules/gramps/gen/lib/tagbase.html#TagBase.serialize)[¶](#gramps.gen.lib.tagbase.TagBase.serialize)
Convert the object to a serialized tuple of data.

`set_tag_list`(*tag_list*)[[source]](../_modules/gramps/gen/lib/tagbase.html#TagBase.set_tag_list)[¶](#gramps.gen.lib.tagbase.TagBase.set_tag_list)
Assign the passed list to the objects’s list of tags.

Parameters
**tag_list** (*list*) – List of tags to ba associated with the object.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/tagbase.html#TagBase.unserialize)[¶](#gramps.gen.lib.tagbase.TagBase.unserialize)
Convert a serialized tuple of data to an object.

### UrlBase[¶](#module-gramps.gen.lib.urlbase)
UrlBase class for Gramps.

*class *`gramps.gen.lib.urlbase.``UrlBase`(*source=None*)[[source]](../_modules/gramps/gen/lib/urlbase.html#UrlBase)[¶](#gramps.gen.lib.urlbase.UrlBase)
Bases: `object`

Base class for url-aware objects.

`add_url`(*url*)[[source]](../_modules/gramps/gen/lib/urlbase.html#UrlBase.add_url)[¶](#gramps.gen.lib.urlbase.UrlBase.add_url)
Add a [`Url`](#gramps.gen.lib.url.Url) instance to the object’s list of
[`Url`](#gramps.gen.lib.url.Url) instances.

Parameters
**url** ([`Url`](#gramps.gen.lib.url.Url)) – [`Url`](#gramps.gen.lib.url.Url) instance to be added to the Person’s
list of related web sites.

`get_url_list`()[[source]](../_modules/gramps/gen/lib/urlbase.html#UrlBase.get_url_list)[¶](#gramps.gen.lib.urlbase.UrlBase.get_url_list)
Return the list of [`Url`](#gramps.gen.lib.url.Url) instances associated with the
object.

Returns
List of [`Url`](#gramps.gen.lib.url.Url) instances

Return type
list

`remove_url`(*url*)[[source]](../_modules/gramps/gen/lib/urlbase.html#UrlBase.remove_url)[¶](#gramps.gen.lib.urlbase.UrlBase.remove_url)
Remove the specified [`Url`](#gramps.gen.lib.url.Url) instance from the url list.

If the instance does not exist in the list, the operation has no effect.

Parameters
**url** ([`Url`](#gramps.gen.lib.url.Url)) – [`Url`](#gramps.gen.lib.url.Url) instance to remove from the list

Returns
True if the url was removed, False if it was not in the list.

Return type
bool

`serialize`()[[source]](../_modules/gramps/gen/lib/urlbase.html#UrlBase.serialize)[¶](#gramps.gen.lib.urlbase.UrlBase.serialize)
Convert the object to a serialized tuple of data

`set_url_list`(*url_list*)[[source]](../_modules/gramps/gen/lib/urlbase.html#UrlBase.set_url_list)[¶](#gramps.gen.lib.urlbase.UrlBase.set_url_list)
Set the list of [`Url`](#gramps.gen.lib.url.Url) instances to passed the list.

Parameters
**url_list** (*list*) – List of [`Url`](#gramps.gen.lib.url.Url) instances

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/urlbase.html#UrlBase.unserialize)[¶](#gramps.gen.lib.urlbase.UrlBase.unserialize)
Convert a serialized tuple of data to an object.

## Primary objects[¶](#primary-objects)

### BasicPrimaryObject[¶](#module-gramps.gen.lib.primaryobj)
Basic Primary Object class for Gramps.

*class *`gramps.gen.lib.primaryobj.``BasicPrimaryObject`(*source=None*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject)
Bases: [`gramps.gen.lib.tableobj.TableObject`](#gramps.gen.lib.tableobj.TableObject), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase), [`gramps.gen.lib.tagbase.TagBase`](#gramps.gen.lib.tagbase.TagBase)

The BasicPrimaryObject is the base class for [`Note`](#gramps.gen.lib.note.Note) objects.

It is also the base class for the [`PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject) class.

The [`PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject) is the base class for all other primary objects
in the database. Primary objects are the core objects in the database.
Each object has a database handle and a Gramps ID value. The database
handle is used as the record number for the database, and the Gramps
ID is the user visible version.

`get_gramps_id`()[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.get_gramps_id)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.get_gramps_id)
Return the Gramps ID for the primary object.

Returns
Gramps ID associated with the object

Return type
str

`has_citation_reference`(*handle*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.has_citation_reference)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.has_citation_reference)
Indicate if the object has a citation references.

In the base class, no such references exist. Derived classes should
override this if they provide citation references.

`has_handle_reference`(*classname*, *handle*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.has_handle_reference)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.has_handle_reference)
Return True if the object has reference to a given handle of given
primary object type.

Parameters

- **classname** (*str*) – The name of the primary object class.

- **handle** (*str*) – The handle to be checked.

Returns
Returns whether the object has reference to this handle of
this object type.

Return type
bool

`has_media_reference`(*handle*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.has_media_reference)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.has_media_reference)
Indicate if the object has a media references.

In the base class, no such references exist. Derived classes should
override this if they provide media references.

`remove_citation_references`(*handle_list*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.remove_citation_references)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.remove_citation_references)
Remove the specified citation references from the object.

In the base class no such references exist. Derived classes should
override this if they provide citation references.

`remove_handle_references`(*classname*, *handle_list*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.remove_handle_references)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.remove_handle_references)
Remove all references in this object to object handles in the list.

Parameters

- **classname** (*str*) – The name of the primary object class.

- **handle_list** (*str*) – The list of handles to be removed.

`remove_media_references`(*handle_list*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.remove_media_references)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.remove_media_references)
Remove the specified media references from the object.

In the base class no such references exist. Derived classes should
override this if they provide media references.

`replace_citation_references`(*old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.replace_citation_references)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.replace_citation_references)
Replace all references to the old citation handle with those to the new
citation handle.

`replace_handle_reference`(*classname*, *old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.replace_handle_reference)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.replace_handle_reference)
Replace all references to old handle with those to the new handle.

Parameters

- **classname** (*str*) – The name of the primary object class.

- **old_handle** (*str*) – The handle to be replaced.

- **new_handle** (*str*) – The handle to replace the old one with.

`replace_media_references`(*old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.replace_media_references)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.replace_media_references)
Replace all references to the old media handle with those to the new
media handle.

`serialize`()[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.serialize)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.serialize)
Convert the object to a serialized tuple of data.

`set_gramps_id`(*gramps_id*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.set_gramps_id)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.set_gramps_id)
Set the Gramps ID for the primary object.

Parameters
**gramps_id** (*str*) – Gramps ID

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#BasicPrimaryObject.unserialize)[¶](#gramps.gen.lib.primaryobj.BasicPrimaryObject.unserialize)
Convert a serialized tuple of data to an object.

### PrimaryObject[¶](#primaryobject)

*class *`gramps.gen.lib.primaryobj.``PrimaryObject`(*source=None*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#PrimaryObject)[¶](#gramps.gen.lib.primaryobj.PrimaryObject)
Bases: [`gramps.gen.lib.primaryobj.BasicPrimaryObject`](#gramps.gen.lib.primaryobj.BasicPrimaryObject)

The PrimaryObject is the base class for all primary objects in the
database.

Primary objects are the core objects in the database.
Each object has a database handle and a Gramps ID value. The database
handle is used as the record number for the database, and the Gramps
ID is the user visible version.

`has_handle_reference`(*classname*, *handle*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#PrimaryObject.has_handle_reference)[¶](#gramps.gen.lib.primaryobj.PrimaryObject.has_handle_reference)
Return True if the object has reference to a given handle of given
primary object type.

Parameters

- **classname** (*str*) – The name of the primary object class.

- **handle** (*str*) – The handle to be checked.

Returns
Returns whether the object has reference to this handle
of this object type.

Return type
bool

`remove_handle_references`(*classname*, *handle_list*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#PrimaryObject.remove_handle_references)[¶](#gramps.gen.lib.primaryobj.PrimaryObject.remove_handle_references)
Remove all references in this object to object handles in the list.

Parameters

- **classname** (*str*) – The name of the primary object class.

- **handle_list** (*str*) – The list of handles to be removed.

`replace_handle_reference`(*classname*, *old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#PrimaryObject.replace_handle_reference)[¶](#gramps.gen.lib.primaryobj.PrimaryObject.replace_handle_reference)
Replace all references to old handle with those to the new handle.

Parameters

- **classname** (*str*) – The name of the primary object class.

- **old_handle** (*str*) – The handle to be replaced.

- **new_handle** (*str*) – The handle to replace the old one with.

`serialize`()[[source]](../_modules/gramps/gen/lib/primaryobj.html#PrimaryObject.serialize)[¶](#gramps.gen.lib.primaryobj.PrimaryObject.serialize)
Convert the object to a serialized tuple of data.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/primaryobj.html#PrimaryObject.unserialize)[¶](#gramps.gen.lib.primaryobj.PrimaryObject.unserialize)
Convert a serialized tuple of data to an object.

### Person[¶](#module-gramps.gen.lib.person)
Person object for Gramps.

*class *`gramps.gen.lib.person.``Person`(*data=None*)[[source]](../_modules/gramps/gen/lib/person.html#Person)[¶](#gramps.gen.lib.person.Person)
Bases: [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.attrbase.AttributeBase`](#gramps.gen.lib.attrbase.AttributeBase), [`gramps.gen.lib.mediabase.MediaBase`](#gramps.gen.lib.mediabase.MediaBase), [`gramps.gen.lib.addressbase.AddressBase`](#gramps.gen.lib.addressbase.AddressBase), [`gramps.gen.lib.urlbase.UrlBase`](#gramps.gen.lib.urlbase.UrlBase), [`gramps.gen.lib.ldsordbase.LdsOrdBase`](#gramps.gen.lib.ldsordbase.LdsOrdBase), [`gramps.gen.lib.primaryobj.PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject)

The Person record is the Gramps in-memory representation of an
individual person. It contains all the information related to
an individual.

Person objects are usually created in one of two ways.

- Creating a new person object, which is then initialized and added to
the database.

- Retrieving an object from the database using the records handle.

Once a Person object has been modified, it must be committed
to the database using the database object’s commit_person function,
or the changes will be lost.

`FEMALE`* = 0*[¶](#gramps.gen.lib.person.Person.FEMALE)

`MALE`* = 1*[¶](#gramps.gen.lib.person.Person.MALE)

`UNKNOWN`* = 2*[¶](#gramps.gen.lib.person.Person.UNKNOWN)

`add_alternate_name`(*name*)[[source]](../_modules/gramps/gen/lib/person.html#Person.add_alternate_name)[¶](#gramps.gen.lib.person.Person.add_alternate_name)
Add a [`Name`](#gramps.gen.lib.name.Name) instance to the list of alternative names.

Parameters
**name** ([`Name`](#gramps.gen.lib.name.Name)) – [`Name`](#gramps.gen.lib.name.Name) to add to the list

`add_event_ref`(*event_ref*)[[source]](../_modules/gramps/gen/lib/person.html#Person.add_event_ref)[¶](#gramps.gen.lib.person.Person.add_event_ref)
Add the [`EventRef`](#gramps.gen.lib.eventref.EventRef) to the Person instance’s
[`EventRef`](#gramps.gen.lib.eventref.EventRef) list.

This is accomplished by assigning the [`EventRef`](#gramps.gen.lib.eventref.EventRef) of a
valid [`Event`](#gramps.gen.lib.event.Event) in the current database.

Parameters
**event_ref** ([*EventRef*](#gramps.gen.lib.eventref.EventRef)) – the [`EventRef`](#gramps.gen.lib.eventref.EventRef) to be added to the
Person’s [`EventRef`](#gramps.gen.lib.eventref.EventRef) list.

`add_family_handle`(*family_handle*)[[source]](../_modules/gramps/gen/lib/person.html#Person.add_family_handle)[¶](#gramps.gen.lib.person.Person.add_family_handle)
Add the [`Family`](#gramps.gen.lib.family.Family) handle to the Person instance’s
[`Family`](#gramps.gen.lib.family.Family) list.

This is accomplished by assigning the handle of a valid
[`Family`](#gramps.gen.lib.family.Family) in the current database.

Adding a [`Family`](#gramps.gen.lib.family.Family) handle to a Person does not
automatically update the corresponding [`Family`](#gramps.gen.lib.family.Family). The
developer is responsible to make sure that when a
[`Family`](#gramps.gen.lib.family.Family) is added to Person, that the Person is assigned
to either the father or mother role in the [`Family`](#gramps.gen.lib.family.Family).

Parameters
**family_handle** (*str*) – handle of the [`Family`](#gramps.gen.lib.family.Family) to be added
to the Person’s [`Family`](#gramps.gen.lib.family.Family) list.

`add_parent_family_handle`(*family_handle*)[[source]](../_modules/gramps/gen/lib/person.html#Person.add_parent_family_handle)[¶](#gramps.gen.lib.person.Person.add_parent_family_handle)
Add the [`Family`](#gramps.gen.lib.family.Family) handle to the Person instance’s list of
families in which it is a child.

This is accomplished by assigning the handle of a valid
[`Family`](#gramps.gen.lib.family.Family) in the current database.

Adding a [`Family`](#gramps.gen.lib.family.Family) handle to a Person does not
automatically update the corresponding [`Family`](#gramps.gen.lib.family.Family). The
developer is responsible to make sure that when a
[`Family`](#gramps.gen.lib.family.Family) is added to Person, that the Person is
added to the [`Family`](#gramps.gen.lib.family.Family) instance’s child list.

Parameters
**family_handle** (*str*) – handle of the [`Family`](#gramps.gen.lib.family.Family) to be added
to the Person’s [`Family`](#gramps.gen.lib.family.Family) list.

`add_person_ref`(*person_ref*)[[source]](../_modules/gramps/gen/lib/person.html#Person.add_person_ref)[¶](#gramps.gen.lib.person.Person.add_person_ref)
Add the [`PersonRef`](#gramps.gen.lib.personref.PersonRef) to the Person instance’s
[`PersonRef`](#gramps.gen.lib.personref.PersonRef) list.

Parameters
**person_ref** ([*PersonRef*](#gramps.gen.lib.personref.PersonRef)) – the [`PersonRef`](#gramps.gen.lib.personref.PersonRef) to be added to the
Person’s [`PersonRef`](#gramps.gen.lib.personref.PersonRef) list.

`clear_family_handle_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.clear_family_handle_list)[¶](#gramps.gen.lib.person.Person.clear_family_handle_list)
Remove all [`Family`](#gramps.gen.lib.family.Family) handles from the
[`Family`](#gramps.gen.lib.family.Family) list.

`clear_parent_family_handle_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.clear_parent_family_handle_list)[¶](#gramps.gen.lib.person.Person.clear_parent_family_handle_list)
Remove all [`Family`](#gramps.gen.lib.family.Family) handles from the parent
[`Family`](#gramps.gen.lib.family.Family) list.

`gender`[¶](#gramps.gen.lib.person.Person.gender)
Returns or sets the gender of the person

`get_alternate_names`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_alternate_names)[¶](#gramps.gen.lib.person.Person.get_alternate_names)
Return the list of alternate [`Name`](#gramps.gen.lib.name.Name) instances.

Returns
List of [`Name`](#gramps.gen.lib.name.Name) instances

Return type
list

`get_birth_ref`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_birth_ref)[¶](#gramps.gen.lib.person.Person.get_birth_ref)
Return the [`EventRef`](#gramps.gen.lib.eventref.EventRef) for Person’s birth event.

This should correspond to an [`Event`](#gramps.gen.lib.event.Event) in the database’s
[`Event`](#gramps.gen.lib.event.Event) list.

Returns
Returns the birth [`EventRef`](#gramps.gen.lib.eventref.EventRef) or None if no
birth [`Event`](#gramps.gen.lib.event.Event) has been assigned.

Return type
[EventRef](#gramps.gen.lib.eventref.EventRef)

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_citation_child_list)[¶](#gramps.gen.lib.person.Person.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_death_ref`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_death_ref)[¶](#gramps.gen.lib.person.Person.get_death_ref)
Return the [`EventRef`](#gramps.gen.lib.eventref.EventRef) for the Person’s death event.

This should correspond to an [`Event`](#gramps.gen.lib.event.Event) in the database’s
[`Event`](#gramps.gen.lib.event.Event) list.

Returns
Returns the death [`EventRef`](#gramps.gen.lib.eventref.EventRef) or None if no
death [`Event`](#gramps.gen.lib.event.Event) has been assigned.

Return type
event_ref

`get_event_ref_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_event_ref_list)[¶](#gramps.gen.lib.person.Person.get_event_ref_list)
Return the list of [`EventRef`](#gramps.gen.lib.eventref.EventRef) objects associated with
[`Event`](#gramps.gen.lib.event.Event) instances.

Returns
Returns the list of [`EventRef`](#gramps.gen.lib.eventref.EventRef) objects
associated with the Person instance.

Return type
list

`get_family_handle_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_family_handle_list)[¶](#gramps.gen.lib.person.Person.get_family_handle_list)
Return the list of [`Family`](#gramps.gen.lib.family.Family) handles in which the person
is a parent or spouse.

Returns
Returns the list of handles corresponding to the
[`Family`](#gramps.gen.lib.family.Family) records with which the person
is associated.

Return type
list

`get_gender`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_gender)[¶](#gramps.gen.lib.person.Person.get_gender)
Return the gender of the Person.

Returns
Returns one of the following constants:

- Person.MALE

- Person.FEMALE

- Person.UNKNOWN

Return type
int

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_handle_referents)[¶](#gramps.gen.lib.person.Person.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_main_parents_family_handle`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_main_parents_family_handle)[¶](#gramps.gen.lib.person.Person.get_main_parents_family_handle)
Return the handle of the [`Family`](#gramps.gen.lib.family.Family) considered to be the
main [`Family`](#gramps.gen.lib.family.Family) in which the Person is a child.

Returns
Returns the family_handle if a family_handle exists,
If no [`Family`](#gramps.gen.lib.family.Family) is assigned, None is returned

Return type
str

`get_nick_name`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_nick_name)[¶](#gramps.gen.lib.person.Person.get_nick_name)

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_note_child_list)[¶](#gramps.gen.lib.person.Person.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_parent_family_handle_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_parent_family_handle_list)[¶](#gramps.gen.lib.person.Person.get_parent_family_handle_list)
Return the list of [`Family`](#gramps.gen.lib.family.Family) handles in which the person
is a child.

Returns
Returns the list of handles corresponding to the
[`Family`](#gramps.gen.lib.family.Family) records with which the person is a
child.

Return type
list

`get_person_ref_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_person_ref_list)[¶](#gramps.gen.lib.person.Person.get_person_ref_list)
Return the list of [`PersonRef`](#gramps.gen.lib.personref.PersonRef) objects.

Returns
Returns the list of [`PersonRef`](#gramps.gen.lib.personref.PersonRef) objects.

Return type
list

`get_primary_event_ref_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_primary_event_ref_list)[¶](#gramps.gen.lib.person.Person.get_primary_event_ref_list)
Return the list of [`EventRef`](#gramps.gen.lib.eventref.EventRef) objects associated with
[`Event`](#gramps.gen.lib.event.Event) instances that have been marked as primary
events.

Returns
Returns generator of [`EventRef`](#gramps.gen.lib.eventref.EventRef) objects
associated with the Person instance.

Return type
generator

`get_primary_name`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_primary_name)[¶](#gramps.gen.lib.person.Person.get_primary_name)
Return the [`Name`](#gramps.gen.lib.name.Name) instance marked as the Person’s primary
name.

Returns
Returns the primary name

Return type
[`Name`](#gramps.gen.lib.name.Name)

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_referenced_handles)[¶](#gramps.gen.lib.person.Person.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_schema)[¶](#gramps.gen.lib.person.Person.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_text_data_child_list)[¶](#gramps.gen.lib.person.Person.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/person.html#Person.get_text_data_list)[¶](#gramps.gen.lib.person.Person.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/person.html#Person.merge)[¶](#gramps.gen.lib.person.Person.merge)
Merge the content of acquisition into this person.

Parameters
**acquisition** ([*Person*](#gramps.gen.lib.person.Person)) – The person to merge with the present person.

`remove_family_handle`(*family_handle*)[[source]](../_modules/gramps/gen/lib/person.html#Person.remove_family_handle)[¶](#gramps.gen.lib.person.Person.remove_family_handle)
Remove the specified [`Family`](#gramps.gen.lib.family.Family) handle from the list of
marriages/partnerships.

If the handle does not exist in the list, the operation has no effect.

Parameters
**family_handle** (*str*) – [`Family`](#gramps.gen.lib.family.Family) handle to remove from
the list

Returns
True if the handle was removed, False if it was not
in the list.

Return type
bool

`remove_parent_family_handle`(*family_handle*)[[source]](../_modules/gramps/gen/lib/person.html#Person.remove_parent_family_handle)[¶](#gramps.gen.lib.person.Person.remove_parent_family_handle)
Remove the specified [`Family`](#gramps.gen.lib.family.Family) handle from the list of
parent families (families in which the parent is a child).

If the handle does not exist in the list, the operation has no effect.

Parameters
**family_handle** (*str*) – [`Family`](#gramps.gen.lib.family.Family) handle to remove from the
list

Returns
Returns a tuple of three strings, consisting of the
removed handle, relationship to mother, and relationship
to father. None is returned if the handle is not in the
list.

Return type
tuple

`serialize`()[[source]](../_modules/gramps/gen/lib/person.html#Person.serialize)[¶](#gramps.gen.lib.person.Person.serialize)
Convert the data held in the Person to a Python tuple that
represents all the data elements.

This method is used to convert the object into a form that can easily
be saved to a database.

These elements may be primitive Python types (string, integers),
complex Python types (lists or tuples, or Python objects. If the
target database cannot handle complex types (such as objects or
lists), the database is responsible for converting the data into
a form that it can use.

Returns
Returns a python tuple containing the data that should
be considered persistent.

Return type
tuple

`set_alternate_names`(*alt_name_list*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_alternate_names)[¶](#gramps.gen.lib.person.Person.set_alternate_names)
Change the list of alternate names to the passed list.

Parameters
**alt_name_list** (*list*) – List of [`Name`](#gramps.gen.lib.name.Name) instances

`set_birth_ref`(*event_ref*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_birth_ref)[¶](#gramps.gen.lib.person.Person.set_birth_ref)
Assign the birth event to the Person object.

This is accomplished by assigning the [`EventRef`](#gramps.gen.lib.eventref.EventRef) of
the birth event in the current database.

Parameters
**event_ref** ([*EventRef*](#gramps.gen.lib.eventref.EventRef)) – the [`EventRef`](#gramps.gen.lib.eventref.EventRef) object associated
with the Person’s birth.

`set_death_ref`(*event_ref*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_death_ref)[¶](#gramps.gen.lib.person.Person.set_death_ref)
Assign the death event to the Person object.

This is accomplished by assigning the [`EventRef`](#gramps.gen.lib.eventref.EventRef) of
the death event in the current database.

Parameters
**event_ref** ([*EventRef*](#gramps.gen.lib.eventref.EventRef)) – the [`EventRef`](#gramps.gen.lib.eventref.EventRef) object associated
with the Person’s death.

`set_event_ref_list`(*event_ref_list*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_event_ref_list)[¶](#gramps.gen.lib.person.Person.set_event_ref_list)
Set the Person instance’s [`EventRef`](#gramps.gen.lib.eventref.EventRef) list to the
passed list.

Parameters
**event_ref_list** (*list*) – List of valid [`EventRef`](#gramps.gen.lib.eventref.EventRef)
objects.

`set_family_handle_list`(*family_list*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_family_handle_list)[¶](#gramps.gen.lib.person.Person.set_family_handle_list)
Assign the passed list to the Person’s list of families in which it is
a parent or spouse.

Parameters
**family_list** (*list*) – List of [`Family`](#gramps.gen.lib.family.Family) handles to be
associated with the Person

`set_gender`(*gender*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_gender)[¶](#gramps.gen.lib.person.Person.set_gender)
Set the gender of the Person.

Parameters
**gender** (*int*) – Assigns the Person’s gender to one of the
following constants:

- Person.MALE

- Person.FEMALE

- Person.UNKNOWN

`set_main_parent_family_handle`(*family_handle*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_main_parent_family_handle)[¶](#gramps.gen.lib.person.Person.set_main_parent_family_handle)
Set the main [`Family`](#gramps.gen.lib.family.Family) in which the Person is a child.

The main [`Family`](#gramps.gen.lib.family.Family) is the [`Family`](#gramps.gen.lib.family.Family)
typically used for reports and navigation. This is accomplished by
moving the [`Family`](#gramps.gen.lib.family.Family) to the beginning of the list. The
family_handle must be in the list for this to have any effect.

Parameters
**family_handle** (*str*) – handle of the [`Family`](#gramps.gen.lib.family.Family) to be
marked as the main [`Family`](#gramps.gen.lib.family.Family)

Returns
Returns True if the assignment has successful

Return type
bool

`set_parent_family_handle_list`(*family_list*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_parent_family_handle_list)[¶](#gramps.gen.lib.person.Person.set_parent_family_handle_list)
Return the list of [`Family`](#gramps.gen.lib.family.Family) handles in which the person
is a child.

Returns
Returns the list of handles corresponding to the
[`Family`](#gramps.gen.lib.family.Family) records with which the person is a
child.

Return type
list

`set_person_ref_list`(*person_ref_list*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_person_ref_list)[¶](#gramps.gen.lib.person.Person.set_person_ref_list)
Set the Person instance’s [`PersonRef`](#gramps.gen.lib.personref.PersonRef) list to the
passed list.

Parameters
**person_ref_list** (*list*) – List of valid [`PersonRef`](#gramps.gen.lib.personref.PersonRef)
objects

`set_preferred_family_handle`(*family_handle*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_preferred_family_handle)[¶](#gramps.gen.lib.person.Person.set_preferred_family_handle)
Set the family_handle specified to be the preferred
[`Family`](#gramps.gen.lib.family.Family).

The preferred [`Family`](#gramps.gen.lib.family.Family) is determined by the first
[`Family`](#gramps.gen.lib.family.Family) in the [`Family`](#gramps.gen.lib.family.Family) list, and is
typically used to indicate the preferred [`Family`](#gramps.gen.lib.family.Family) for
navigation or reporting.

The family_handle must already be in the list, or the function
call has no effect.

Parameters
**family_handle** (*str*) – Handle of the [`Family`](#gramps.gen.lib.family.Family) to make the
preferred [`Family`](#gramps.gen.lib.family.Family).

Returns
True if the call succeeded, False if the family_handle
was not already in the [`Family`](#gramps.gen.lib.family.Family) list.

Return type
bool

`set_primary_name`(*name*)[[source]](../_modules/gramps/gen/lib/person.html#Person.set_primary_name)[¶](#gramps.gen.lib.person.Person.set_primary_name)
Set the primary name of the Person to the specified [`Name`](#gramps.gen.lib.name.Name)
instance.

Parameters
**name** ([`Name`](#gramps.gen.lib.name.Name)) – [`Name`](#gramps.gen.lib.name.Name) to be assigned to the person

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/person.html#Person.unserialize)[¶](#gramps.gen.lib.person.Person.unserialize)
Convert the data held in a tuple created by the serialize method
back into the data in a Person object.

Parameters
**data** (*tuple*) – tuple containing the persistent data associated the
Person object

### Family[¶](#module-gramps.gen.lib.family)
Family object for Gramps.

*class *`gramps.gen.lib.family.``Family`[[source]](../_modules/gramps/gen/lib/family.html#Family)[¶](#gramps.gen.lib.family.Family)
Bases: [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.mediabase.MediaBase`](#gramps.gen.lib.mediabase.MediaBase), [`gramps.gen.lib.attrbase.AttributeBase`](#gramps.gen.lib.attrbase.AttributeBase), [`gramps.gen.lib.ldsordbase.LdsOrdBase`](#gramps.gen.lib.ldsordbase.LdsOrdBase), [`gramps.gen.lib.primaryobj.PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject)

The Family record is the Gramps in-memory representation of the
relationships between people. It contains all the information
related to the relationship.

Family objects are usually created in one of two ways.

- Creating a new Family object, which is then initialized and
added to the database.

- Retrieving an object from the database using the records
handle.

Once a Family object has been modified, it must be committed
to the database using the database object’s commit_family function,
or the changes will be lost.

`add_child_ref`(*child_ref*)[[source]](../_modules/gramps/gen/lib/family.html#Family.add_child_ref)[¶](#gramps.gen.lib.family.Family.add_child_ref)
Add the database handle for [`Person`](#gramps.gen.lib.person.Person) to the Family’s
list of children.

Parameters
**child_ref** ([*ChildRef*](#gramps.gen.lib.childref.ChildRef)) – Child Reference instance

`add_event_ref`(*event_ref*)[[source]](../_modules/gramps/gen/lib/family.html#Family.add_event_ref)[¶](#gramps.gen.lib.family.Family.add_event_ref)
Add the [`EventRef`](#gramps.gen.lib.eventref.EventRef) to the Family instance’s
[`EventRef`](#gramps.gen.lib.eventref.EventRef) list.

This is accomplished by assigning the [`EventRef`](#gramps.gen.lib.eventref.EventRef) for
the valid [`Event`](#gramps.gen.lib.event.Event) in the current database.

Parameters
**event_ref** ([*EventRef*](#gramps.gen.lib.eventref.EventRef)) – the [`EventRef`](#gramps.gen.lib.eventref.EventRef) to be added to the
Person’s [`EventRef`](#gramps.gen.lib.eventref.EventRef) list.

`get_child_ref_list`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_child_ref_list)[¶](#gramps.gen.lib.family.Family.get_child_ref_list)
Return the list of [`ChildRef`](#gramps.gen.lib.childref.ChildRef) handles identifying the
children of the Family.

Returns
Returns the list of [`ChildRef`](#gramps.gen.lib.childref.ChildRef) handles
associated with the Family.

Return type
list

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_citation_child_list)[¶](#gramps.gen.lib.family.Family.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_event_list`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_event_list)[¶](#gramps.gen.lib.family.Family.get_event_list)

`get_event_ref_list`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_event_ref_list)[¶](#gramps.gen.lib.family.Family.get_event_ref_list)
Return the list of [`EventRef`](#gramps.gen.lib.eventref.EventRef) objects associated with
[`Event`](#gramps.gen.lib.event.Event) instances.

Returns
Returns the list of [`EventRef`](#gramps.gen.lib.eventref.EventRef) objects
associated with the Family instance.

Return type
list

`get_father_handle`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_father_handle)[¶](#gramps.gen.lib.family.Family.get_father_handle)
Return the database handle of the [`Person`](#gramps.gen.lib.person.Person) identified
as the father of the Family.

Returns
[`Person`](#gramps.gen.lib.person.Person) database handle

Return type
str

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_handle_referents)[¶](#gramps.gen.lib.family.Family.get_handle_referents)
Return the list of child objects which may, directly or through their
children, reference primary objects..

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_mother_handle`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_mother_handle)[¶](#gramps.gen.lib.family.Family.get_mother_handle)
Return the database handle of the [`Person`](#gramps.gen.lib.person.Person) identified
as the mother of the Family.

Returns
[`Person`](#gramps.gen.lib.person.Person) database handle

Return type
str

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_note_child_list)[¶](#gramps.gen.lib.family.Family.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_referenced_handles)[¶](#gramps.gen.lib.family.Family.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

`get_relationship`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_relationship)[¶](#gramps.gen.lib.family.Family.get_relationship)
Return the relationship type between the people identified as the
father and mother in the relationship.

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_schema)[¶](#gramps.gen.lib.family.Family.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_text_data_child_list)[¶](#gramps.gen.lib.family.Family.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/family.html#Family.get_text_data_list)[¶](#gramps.gen.lib.family.Family.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/family.html#Family.merge)[¶](#gramps.gen.lib.family.Family.merge)
Merge the content of acquisition into this family.

Lost: handle, id, relation, father, mother of acquisition.

Parameters
**acquisition** ([*Family*](#gramps.gen.lib.family.Family)) – The family to merge with the present family.

`remove_child_handle`(*child_handle*)[[source]](../_modules/gramps/gen/lib/family.html#Family.remove_child_handle)[¶](#gramps.gen.lib.family.Family.remove_child_handle)
Remove the database handle for [`Person`](#gramps.gen.lib.person.Person) to the Family’s
list of children if the [`Person`](#gramps.gen.lib.person.Person) is already in the list.

Parameters
**child_handle** (*str*) – [`Person`](#gramps.gen.lib.person.Person) database handle

Returns
True if the handle was removed, False if it was not
in the list.

Return type
bool

`remove_child_ref`(*child_ref*)[[source]](../_modules/gramps/gen/lib/family.html#Family.remove_child_ref)[¶](#gramps.gen.lib.family.Family.remove_child_ref)
Remove the database handle for [`Person`](#gramps.gen.lib.person.Person) to the Family’s
list of children if the [`Person`](#gramps.gen.lib.person.Person) is already in the list.

Parameters
**child_ref** ([*ChildRef*](#gramps.gen.lib.childref.ChildRef)) – Child Reference instance

Returns
True if the handle was removed, False if it was not
in the list.

Return type
bool

`serialize`()[[source]](../_modules/gramps/gen/lib/family.html#Family.serialize)[¶](#gramps.gen.lib.family.Family.serialize)
Convert the data held in the event to a Python tuple that
represents all the data elements.

This method is used to convert the object into a form that can easily
be saved to a database.

These elements may be primitive Python types (string, integers),
complex Python types (lists or tuples, or Python objects. If the
target database cannot handle complex types (such as objects or
lists), the database is responsible for converting the data into
a form that it can use.

Returns
Returns a python tuple containing the data that should
be considered persistent.

Return type
tuple

`set_child_ref_list`(*child_ref_list*)[[source]](../_modules/gramps/gen/lib/family.html#Family.set_child_ref_list)[¶](#gramps.gen.lib.family.Family.set_child_ref_list)
Assign the passed list to the Family’s list children.

Parameters
**child_ref_list** (list of [`ChildRef`](#gramps.gen.lib.childref.ChildRef) instances) – List of Child Reference instances to be
associated as the Family’s list of children.

`set_event_ref_list`(*event_ref_list*)[[source]](../_modules/gramps/gen/lib/family.html#Family.set_event_ref_list)[¶](#gramps.gen.lib.family.Family.set_event_ref_list)
Set the Family instance’s [`EventRef`](#gramps.gen.lib.eventref.EventRef) list to the
passed list.

Parameters
**event_ref_list** (*list*) – List of valid [`EventRef`](#gramps.gen.lib.eventref.EventRef)
objects

`set_father_handle`(*person_handle*)[[source]](../_modules/gramps/gen/lib/family.html#Family.set_father_handle)[¶](#gramps.gen.lib.family.Family.set_father_handle)
Set the database handle for [`Person`](#gramps.gen.lib.person.Person) that corresponds
to male of the relationship.

For a same sex relationship, this can represent either of people
involved in the relationship.

Parameters
**person_handle** (*str*) – [`Person`](#gramps.gen.lib.person.Person) database handle

`set_mother_handle`(*person_handle*)[[source]](../_modules/gramps/gen/lib/family.html#Family.set_mother_handle)[¶](#gramps.gen.lib.family.Family.set_mother_handle)
Set the database handle for [`Person`](#gramps.gen.lib.person.Person) that corresponds
to male of the relationship.

For a same sex relationship, this can represent either of people
involved in the relationship.

Parameters
**person_handle** (*str*) – [`Person`](#gramps.gen.lib.person.Person) database handle

`set_relationship`(*relationship_type*)[[source]](../_modules/gramps/gen/lib/family.html#Family.set_relationship)[¶](#gramps.gen.lib.family.Family.set_relationship)
Set the relationship type between the people identified as the
father and mother in the relationship.

The type is a tuple whose first item is an integer constant and whose
second item is the string. The valid values are:

| Table |
|-------|

| Type

 |
Description

 |
 |

| FamilyRelType.MARRIED

 |
indicates a legally recognized married
relationship between two individuals. This
may be either an opposite or a same sex
relationship.

 |
 |
| FamilyRelType.UNMARRIED

 |
indicates a relationship between two
individuals that is not a legally recognized
relationship.

 |
 |
| FamilyRelType.CIVIL_UNION

 |
indicates a legally recongnized, non-married
relationship between two individuals of the
same sex.

 |
 |
| FamilyRelType.UNKNOWN

 |
indicates that the type of relationship
between the two individuals is not know.

 |
 |
| FamilyRelType.CUSTOM

 |
indicates that the type of relationship
between the two individuals does not match
any of the other types.

 |
 |

Parameters
**relationship_type** (*tuple*) – (int,str) tuple of the relationship type
between the father and mother of the relationship.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/family.html#Family.unserialize)[¶](#gramps.gen.lib.family.Family.unserialize)
Convert the data held in a tuple created by the serialize method
back into the data in a Family structure.

### Event[¶](#module-gramps.gen.lib.event)
Event object for Gramps.

*class *`gramps.gen.lib.event.``Event`(*source=None*)[[source]](../_modules/gramps/gen/lib/event.html#Event)[¶](#gramps.gen.lib.event.Event)
Bases: [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.mediabase.MediaBase`](#gramps.gen.lib.mediabase.MediaBase), [`gramps.gen.lib.attrbase.AttributeBase`](#gramps.gen.lib.attrbase.AttributeBase), [`gramps.gen.lib.datebase.DateBase`](#gramps.gen.lib.datebase.DateBase), [`gramps.gen.lib.placebase.PlaceBase`](#gramps.gen.lib.placebase.PlaceBase), [`gramps.gen.lib.primaryobj.PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject)

The Event record is used to store information about some type of
action that occurred at a particular place at a particular time,
such as a birth, death, or marriage.

A possible definition: Events are things that happen at some point in time
(that we may not know precisely, though), at some place, may involve
several people (witnesses, officers, notaries, priests, etc.) and may
of course have sources, notes, media, etc.
Compare this with attribute: [`Attribute`](#gramps.gen.lib.attribute.Attribute)

`are_equal`(*other*)[[source]](../_modules/gramps/gen/lib/event.html#Event.are_equal)[¶](#gramps.gen.lib.event.Event.are_equal)
Return True if the passed Event is equivalent to the current Event.

Parameters
**other** ([*Event*](#gramps.gen.lib.event.Event)) – Event to compare against

Returns
True if the Events are equal

Return type
bool

`description`[¶](#gramps.gen.lib.event.Event.description)
Returns or sets description of the event

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/event.html#Event.get_citation_child_list)[¶](#gramps.gen.lib.event.Event.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_description`()[[source]](../_modules/gramps/gen/lib/event.html#Event.get_description)[¶](#gramps.gen.lib.event.Event.get_description)
Return the description of the Event.

Returns
Returns the description of the Event

Return type
str

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/event.html#Event.get_handle_referents)[¶](#gramps.gen.lib.event.Event.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/event.html#Event.get_note_child_list)[¶](#gramps.gen.lib.event.Event.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/event.html#Event.get_referenced_handles)[¶](#gramps.gen.lib.event.Event.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/event.html#Event.get_schema)[¶](#gramps.gen.lib.event.Event.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/event.html#Event.get_text_data_child_list)[¶](#gramps.gen.lib.event.Event.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/event.html#Event.get_text_data_list)[¶](#gramps.gen.lib.event.Event.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`get_type`()[[source]](../_modules/gramps/gen/lib/event.html#Event.get_type)[¶](#gramps.gen.lib.event.Event.get_type)
Return the type of the Event.

Returns
Type of the Event

Return type
tuple

`is_empty`()[[source]](../_modules/gramps/gen/lib/event.html#Event.is_empty)[¶](#gramps.gen.lib.event.Event.is_empty)
Return True if the Event is an empty object (no values set).

Returns
True if the Event is empty

Return type
bool

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/event.html#Event.merge)[¶](#gramps.gen.lib.event.Event.merge)
Merge the content of acquisition into this event.

Lost: handle, id, marker, type, date, place, description of acquisition.

Parameters
**acquisition** ([*Event*](#gramps.gen.lib.event.Event)) – The event to merge with the present event.

`serialize`(*no_text_date=False*)[[source]](../_modules/gramps/gen/lib/event.html#Event.serialize)[¶](#gramps.gen.lib.event.Event.serialize)
Convert the data held in the event to a Python tuple that
represents all the data elements.

This method is used to convert the object into a form that can easily
be saved to a database.

These elements may be primitive Python types (string, integers),
complex Python types (lists or tuples, or Python objects. If the
target database cannot handle complex types (such as objects or
lists), the database is responsible for converting the data into
a form that it can use.

Returns
Returns a python tuple containing the data that should
be considered persistent.

Return type
tuple

`set_description`(*description*)[[source]](../_modules/gramps/gen/lib/event.html#Event.set_description)[¶](#gramps.gen.lib.event.Event.set_description)
Set the description of the Event to the passed string.

The string may contain any information.

Parameters
**description** (*str*) – Description to assign to the Event

`set_type`(*the_type*)[[source]](../_modules/gramps/gen/lib/event.html#Event.set_type)[¶](#gramps.gen.lib.event.Event.set_type)
Set the type of the Event to the passed (int,str) tuple.

Parameters
**the_type** (*tuple*) – Type to assign to the Event

`type`[¶](#gramps.gen.lib.event.Event.type)
Returns or sets type of the event

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/event.html#Event.unserialize)[¶](#gramps.gen.lib.event.Event.unserialize)
Convert the data held in a tuple created by the serialize method
back into the data in an Event structure.

Parameters
**data** (*tuple*) – tuple containing the persistent data associated with the
Event object

### Place[¶](#module-gramps.gen.lib.place)
Place object for Gramps.

*class *`gramps.gen.lib.place.``Place`(*source=None*)[[source]](../_modules/gramps/gen/lib/place.html#Place)[¶](#gramps.gen.lib.place.Place)
Bases: [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.mediabase.MediaBase`](#gramps.gen.lib.mediabase.MediaBase), [`gramps.gen.lib.urlbase.UrlBase`](#gramps.gen.lib.urlbase.UrlBase), [`gramps.gen.lib.primaryobj.PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject)

Contains information related to a place, including multiple address
information (since place names can change with time), longitude, latitude,
a collection of images and URLs, a note and a source.

`add_alternate_locations`(*location*)[[source]](../_modules/gramps/gen/lib/place.html#Place.add_alternate_locations)[¶](#gramps.gen.lib.place.Place.add_alternate_locations)
Add a [`Location`](#gramps.gen.lib.location.Location) object to the alternate location
list.

Parameters
**location** ([`Location`](#gramps.gen.lib.location.Location)) – [`Location`](#gramps.gen.lib.location.Location) instance to add

`add_alternative_name`(*name*)[[source]](../_modules/gramps/gen/lib/place.html#Place.add_alternative_name)[¶](#gramps.gen.lib.place.Place.add_alternative_name)
Add a name to the alternative names list.

Parameters
**name** (*string*) – name to add

`add_placeref`(*placeref*)[[source]](../_modules/gramps/gen/lib/place.html#Place.add_placeref)[¶](#gramps.gen.lib.place.Place.add_placeref)
Add a place reference to the list of place references.

Parameters
**code** ([*PlaceRef*](#gramps.gen.lib.placeref.PlaceRef)) – place reference to append to the list

`get_all_names`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_all_names)[¶](#gramps.gen.lib.place.Place.get_all_names)
Return a list of all names of the Place object.

Returns
Returns a list of all names of the Place

Return type
list of PlaceName

`get_alternate_locations`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_alternate_locations)[¶](#gramps.gen.lib.place.Place.get_alternate_locations)
Return a list of alternate [`Location`](#gramps.gen.lib.location.Location) objects the
present alternate information about the current Place.

A Place can have more than one [`Location`](#gramps.gen.lib.location.Location), since
names and jurisdictions can change over time for the same place.

Returns
Returns the alternate [`Location`](#gramps.gen.lib.location.Location) objects
for the Place

Return type
list of [`Location`](#gramps.gen.lib.location.Location) objects

`get_alternative_names`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_alternative_names)[¶](#gramps.gen.lib.place.Place.get_alternative_names)
Return a list of alternative names for the current Place.

Returns
Returns the alternative names for the Place

Return type
list of PlaceName

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_citation_child_list)[¶](#gramps.gen.lib.place.Place.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

Returns
List of child secondary child objects that may refer citations.

Return type
list

`get_code`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_code)[¶](#gramps.gen.lib.place.Place.get_code)
Return the code of the Place object.

Returns
Returns the code of the Place

Return type
str

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_handle_referents)[¶](#gramps.gen.lib.place.Place.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_latitude`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_latitude)[¶](#gramps.gen.lib.place.Place.get_latitude)
Return the latitude of the Place object.

Returns
Returns the latitude of the Place

Return type
str

`get_longitude`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_longitude)[¶](#gramps.gen.lib.place.Place.get_longitude)
Return the longitude of the Place object.

Returns
Returns the longitude of the Place

Return type
str

`get_name`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_name)[¶](#gramps.gen.lib.place.Place.get_name)
Return the name of the Place object.

Returns
Returns the name of the Place

Return type
PlaceName

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_note_child_list)[¶](#gramps.gen.lib.place.Place.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_placeref_list`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_placeref_list)[¶](#gramps.gen.lib.place.Place.get_placeref_list)
Return the place reference list for the Place object.

Returns
Returns the place reference list for the Place

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_referenced_handles)[¶](#gramps.gen.lib.place.Place.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_schema)[¶](#gramps.gen.lib.place.Place.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_text_data_child_list)[¶](#gramps.gen.lib.place.Place.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_text_data_list)[¶](#gramps.gen.lib.place.Place.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`get_title`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_title)[¶](#gramps.gen.lib.place.Place.get_title)
Return the descriptive title of the Place object.

Returns
Returns the descriptive title of the Place

Return type
str

`get_type`()[[source]](../_modules/gramps/gen/lib/place.html#Place.get_type)[¶](#gramps.gen.lib.place.Place.get_type)
Return the type of the Place object.

Returns
Returns the type of the Place

Return type
[PlaceType](#gramps.gen.lib.placetype.PlaceType)

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/place.html#Place.merge)[¶](#gramps.gen.lib.place.Place.merge)
Merge the content of acquisition into this place.

Parameters
**acquisition** ([*Place*](#gramps.gen.lib.place.Place)) – The place to merge with the present place.

`serialize`()[[source]](../_modules/gramps/gen/lib/place.html#Place.serialize)[¶](#gramps.gen.lib.place.Place.serialize)
Convert the data held in the Place to a Python tuple that
represents all the data elements.

This method is used to convert the object into a form that can easily
be saved to a database.

These elements may be primitive Python types (string, integers),
complex Python types (lists or tuples, or Python objects. If the
target database cannot handle complex types (such as objects or
lists), the database is responsible for converting the data into
a form that it can use.

Returns
Returns a python tuple containing the data that should
be considered persistent.

Return type
tuple

`set_alternate_locations`(*location_list*)[[source]](../_modules/gramps/gen/lib/place.html#Place.set_alternate_locations)[¶](#gramps.gen.lib.place.Place.set_alternate_locations)
Replace the current alternate [`Location`](#gramps.gen.lib.location.Location) object list
with the new one.

Parameters
**location_list** (list of [`Location`](#gramps.gen.lib.location.Location) objects) – The list of [`Location`](#gramps.gen.lib.location.Location) objects
to assign to the Place’s internal list.

`set_alternative_names`(*name_list*)[[source]](../_modules/gramps/gen/lib/place.html#Place.set_alternative_names)[¶](#gramps.gen.lib.place.Place.set_alternative_names)
Replace the current alternative names list with the new one.

Parameters
**name_list** (*list of PlaceName*) – The list of names to assign to the Place’s internal
list.

`set_code`(*code*)[[source]](../_modules/gramps/gen/lib/place.html#Place.set_code)[¶](#gramps.gen.lib.place.Place.set_code)
Set the code of the Place object.

Parameters
**code** (*str*) – code to assign to the Place

`set_latitude`(*latitude*)[[source]](../_modules/gramps/gen/lib/place.html#Place.set_latitude)[¶](#gramps.gen.lib.place.Place.set_latitude)
Set the latitude of the Place object.

Parameters
**latitude** (*str*) – latitude to assign to the Place

`set_longitude`(*longitude*)[[source]](../_modules/gramps/gen/lib/place.html#Place.set_longitude)[¶](#gramps.gen.lib.place.Place.set_longitude)
Set the longitude of the Place object.

Parameters
**longitude** (*str*) – longitude to assign to the Place

`set_name`(*name*)[[source]](../_modules/gramps/gen/lib/place.html#Place.set_name)[¶](#gramps.gen.lib.place.Place.set_name)
Set the name of the Place object.

Parameters
**name** (*PlaceName*) – name to assign to the Place

`set_placeref_list`(*placeref_list*)[[source]](../_modules/gramps/gen/lib/place.html#Place.set_placeref_list)[¶](#gramps.gen.lib.place.Place.set_placeref_list)
Set the place reference list for the Place object.

Parameters
**code** (*list*) – place reference list to assign to the Place

`set_title`(*title*)[[source]](../_modules/gramps/gen/lib/place.html#Place.set_title)[¶](#gramps.gen.lib.place.Place.set_title)
Set the descriptive title of the Place object.

Parameters
**title** (*str*) – descriptive title to assign to the Place

`set_type`(*place_type*)[[source]](../_modules/gramps/gen/lib/place.html#Place.set_type)[¶](#gramps.gen.lib.place.Place.set_type)
Set the type of the Place object.

Parameters
**type** ([*PlaceType*](#gramps.gen.lib.placetype.PlaceType)) – type to assign to the Place

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/place.html#Place.unserialize)[¶](#gramps.gen.lib.place.Place.unserialize)
Convert the data held in a tuple created by the serialize method
back into the data in a Place object.

Parameters
**data** (*tuple*) – tuple containing the persistent data associated with the
Place object

### Source[¶](#module-gramps.gen.lib.src)
Source object for Gramps.

*class *`gramps.gen.lib.src.``Source`[[source]](../_modules/gramps/gen/lib/src.html#Source)[¶](#gramps.gen.lib.src.Source)
Bases: [`gramps.gen.lib.mediabase.MediaBase`](#gramps.gen.lib.mediabase.MediaBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.attrbase.SrcAttributeBase`](#gramps.gen.lib.attrbase.SrcAttributeBase), [`gramps.gen.lib.citationbase.IndirectCitationBase`](#gramps.gen.lib.citationbase.IndirectCitationBase), [`gramps.gen.lib.primaryobj.PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject)

A record of a source of information.

`add_repo_reference`(*repo_ref*)[[source]](../_modules/gramps/gen/lib/src.html#Source.add_repo_reference)[¶](#gramps.gen.lib.src.Source.add_repo_reference)
Add a [`RepoRef`](#gramps.gen.lib.reporef.RepoRef) instance to the Source’s reporef list.

Parameters
**repo_ref** ([`RepoRef`](#gramps.gen.lib.reporef.RepoRef)) – [`RepoRef`](#gramps.gen.lib.reporef.RepoRef) instance to be added to the
object’s reporef list.

`get_abbreviation`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_abbreviation)[¶](#gramps.gen.lib.src.Source.get_abbreviation)
Return the title abbreviation of the Source.

`get_author`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_author)[¶](#gramps.gen.lib.src.Source.get_author)
Return the author of the Source.

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_citation_child_list)[¶](#gramps.gen.lib.src.Source.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_handle_referents)[¶](#gramps.gen.lib.src.Source.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_note_child_list)[¶](#gramps.gen.lib.src.Source.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_publication_info`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_publication_info)[¶](#gramps.gen.lib.src.Source.get_publication_info)
Return the publication information of the Source.

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_referenced_handles)[¶](#gramps.gen.lib.src.Source.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

`get_reporef_list`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_reporef_list)[¶](#gramps.gen.lib.src.Source.get_reporef_list)
Return the list of [`RepoRef`](#gramps.gen.lib.reporef.RepoRef) instances associated with
the Source.

Returns
list of [`RepoRef`](#gramps.gen.lib.reporef.RepoRef) instances associated with
the Source

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_schema)[¶](#gramps.gen.lib.src.Source.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_text_data_child_list)[¶](#gramps.gen.lib.src.Source.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_text_data_list)[¶](#gramps.gen.lib.src.Source.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`get_title`()[[source]](../_modules/gramps/gen/lib/src.html#Source.get_title)[¶](#gramps.gen.lib.src.Source.get_title)
Return the descriptive title of the Place object.

Returns
Returns the descriptive title of the Place

Return type
str

`has_repo_reference`(*repo_handle*)[[source]](../_modules/gramps/gen/lib/src.html#Source.has_repo_reference)[¶](#gramps.gen.lib.src.Source.has_repo_reference)
Return True if the Source has reference to this Repository handle.

Parameters
**repo_handle** (*str*) – The Repository handle to be checked.

Returns
Returns whether the Source has reference to this Repository
handle.

Return type
bool

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/src.html#Source.merge)[¶](#gramps.gen.lib.src.Source.merge)
Merge the content of acquisition into this source.

Parameters
**acquisition** ([*Source*](#gramps.gen.lib.src.Source)) – The source to merge with the present source.

`remove_repo_references`(*repo_handle_list*)[[source]](../_modules/gramps/gen/lib/src.html#Source.remove_repo_references)[¶](#gramps.gen.lib.src.Source.remove_repo_references)
Remove references to all Repository handles in the list.

Parameters
**repo_handle_list** (*list*) – The list of Repository handles to be removed.

`replace_repo_references`(*old_handle*, *new_handle*)[[source]](../_modules/gramps/gen/lib/src.html#Source.replace_repo_references)[¶](#gramps.gen.lib.src.Source.replace_repo_references)
Replace all references to old Repository handle with the new handle
and merge equivalent entries.

Parameters

- **old_handle** (*str*) – The Repository handle to be replaced.

- **new_handle** (*str*) – The Repository handle to replace the old one with.

`serialize`()[[source]](../_modules/gramps/gen/lib/src.html#Source.serialize)[¶](#gramps.gen.lib.src.Source.serialize)
Convert the object to a serialized tuple of data.

`set_abbreviation`(*abbrev*)[[source]](../_modules/gramps/gen/lib/src.html#Source.set_abbreviation)[¶](#gramps.gen.lib.src.Source.set_abbreviation)
Set the title abbreviation of the Source.

`set_author`(*author*)[[source]](../_modules/gramps/gen/lib/src.html#Source.set_author)[¶](#gramps.gen.lib.src.Source.set_author)
Set the author of the Source.

`set_publication_info`(*text*)[[source]](../_modules/gramps/gen/lib/src.html#Source.set_publication_info)[¶](#gramps.gen.lib.src.Source.set_publication_info)
Set the publication information of the Source.

`set_reporef_list`(*reporef_list*)[[source]](../_modules/gramps/gen/lib/src.html#Source.set_reporef_list)[¶](#gramps.gen.lib.src.Source.set_reporef_list)
Set the list of [`RepoRef`](#gramps.gen.lib.reporef.RepoRef) instances associated with
the Source. It replaces the previous list.

Parameters
**reporef_list** (*list*) – list of [`RepoRef`](#gramps.gen.lib.reporef.RepoRef) instances to be
assigned to the Source.

`set_title`(*title*)[[source]](../_modules/gramps/gen/lib/src.html#Source.set_title)[¶](#gramps.gen.lib.src.Source.set_title)
Set the descriptive title of the Source object.

Parameters
**title** (*str*) – descriptive title to assign to the Source

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/src.html#Source.unserialize)[¶](#gramps.gen.lib.src.Source.unserialize)
Convert the data held in a tuple created by the serialize method
back into the data in a Source structure.

### Citation[¶](#module-gramps.gen.lib.citation)
Citation object for Gramps.

*class *`gramps.gen.lib.citation.``Citation`[[source]](../_modules/gramps/gen/lib/citation.html#Citation)[¶](#gramps.gen.lib.citation.Citation)
Bases: [`gramps.gen.lib.mediabase.MediaBase`](#gramps.gen.lib.mediabase.MediaBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.attrbase.SrcAttributeBase`](#gramps.gen.lib.attrbase.SrcAttributeBase), [`gramps.gen.lib.citationbase.IndirectCitationBase`](#gramps.gen.lib.citationbase.IndirectCitationBase), [`gramps.gen.lib.datebase.DateBase`](#gramps.gen.lib.datebase.DateBase), [`gramps.gen.lib.primaryobj.PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject)

A record of a citation of a source of information.

In GEDCOM this is called a SOURCE_CITATION.
The data provided in the > structure is source-related
information specific to the data being cited.

`CONF_HIGH`* = 3*[¶](#gramps.gen.lib.citation.Citation.CONF_HIGH)

`CONF_LOW`* = 1*[¶](#gramps.gen.lib.citation.Citation.CONF_LOW)

`CONF_NORMAL`* = 2*[¶](#gramps.gen.lib.citation.Citation.CONF_NORMAL)

`CONF_VERY_HIGH`* = 4*[¶](#gramps.gen.lib.citation.Citation.CONF_VERY_HIGH)

`CONF_VERY_LOW`* = 0*[¶](#gramps.gen.lib.citation.Citation.CONF_VERY_LOW)

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_citation_child_list)[¶](#gramps.gen.lib.citation.Citation.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_confidence_level`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_confidence_level)[¶](#gramps.gen.lib.citation.Citation.get_confidence_level)
Return the confidence level.

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_handle_referents)[¶](#gramps.gen.lib.citation.Citation.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_note_child_list)[¶](#gramps.gen.lib.citation.Citation.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_page`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_page)[¶](#gramps.gen.lib.citation.Citation.get_page)
Get the page indicator of the Citation.

`get_reference_handle`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_reference_handle)[¶](#gramps.gen.lib.citation.Citation.get_reference_handle)

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_referenced_handles)[¶](#gramps.gen.lib.citation.Citation.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_schema)[¶](#gramps.gen.lib.citation.Citation.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_text_data_child_list)[¶](#gramps.gen.lib.citation.Citation.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/citation.html#Citation.get_text_data_list)[¶](#gramps.gen.lib.citation.Citation.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/citation.html#Citation.merge)[¶](#gramps.gen.lib.citation.Citation.merge)
Merge the content of acquisition into this citation.

Parameters
**acquisition** ([*Citation*](#gramps.gen.lib.citation.Citation)) – The citation to merge with the present citation.

`serialize`(*no_text_date=False*)[[source]](../_modules/gramps/gen/lib/citation.html#Citation.serialize)[¶](#gramps.gen.lib.citation.Citation.serialize)
Convert the object to a serialized tuple of data.

`set_confidence_level`(*val*)[[source]](../_modules/gramps/gen/lib/citation.html#Citation.set_confidence_level)[¶](#gramps.gen.lib.citation.Citation.set_confidence_level)
Set the confidence level.

`set_page`(*page*)[[source]](../_modules/gramps/gen/lib/citation.html#Citation.set_page)[¶](#gramps.gen.lib.citation.Citation.set_page)
Set the page indicator of the Citation.

`set_reference_handle`(*val*)[[source]](../_modules/gramps/gen/lib/citation.html#Citation.set_reference_handle)[¶](#gramps.gen.lib.citation.Citation.set_reference_handle)

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/citation.html#Citation.unserialize)[¶](#gramps.gen.lib.citation.Citation.unserialize)
Convert the data held in a tuple created by the serialize method
back into the data in a Citation structure.

### Media[¶](#module-gramps.gen.lib.media)
Media object for Gramps.

*class *`gramps.gen.lib.media.``Media`(*source=None*)[[source]](../_modules/gramps/gen/lib/media.html#Media)[¶](#gramps.gen.lib.media.Media)
Bases: [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.datebase.DateBase`](#gramps.gen.lib.datebase.DateBase), [`gramps.gen.lib.attrbase.AttributeBase`](#gramps.gen.lib.attrbase.AttributeBase), [`gramps.gen.lib.primaryobj.PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject)

Container for information about an image file, including location,
description and privacy.

`get_checksum`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_checksum)[¶](#gramps.gen.lib.media.Media.get_checksum)
Return the checksum of the image.

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_citation_child_list)[¶](#gramps.gen.lib.media.Media.get_citation_child_list)
Return the list of child secondary objects that may refer to citations.

Returns
Returns the list of child secondary child objects that may
refer to citations.

Return type
list

`get_description`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_description)[¶](#gramps.gen.lib.media.Media.get_description)
Return the description of the image.

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_handle_referents)[¶](#gramps.gen.lib.media.Media.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_mime_type`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_mime_type)[¶](#gramps.gen.lib.media.Media.get_mime_type)
Return the MIME type associated with the Media.

Returns
Returns the associated MIME type

Return type
str

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_note_child_list)[¶](#gramps.gen.lib.media.Media.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_path`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_path)[¶](#gramps.gen.lib.media.Media.get_path)
Return the file path.

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_referenced_handles)[¶](#gramps.gen.lib.media.Media.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_schema)[¶](#gramps.gen.lib.media.Media.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_text_data_child_list)[¶](#gramps.gen.lib.media.Media.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/media.html#Media.get_text_data_list)[¶](#gramps.gen.lib.media.Media.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/media.html#Media.merge)[¶](#gramps.gen.lib.media.Media.merge)
Merge the content of acquisition into this media object.

Lost: handle, id, file, date of acquisition.

Parameters
**acquisition** ([*Media*](#gramps.gen.lib.media.Media)) – The media object to merge with the present object.

`serialize`(*no_text_date=False*)[[source]](../_modules/gramps/gen/lib/media.html#Media.serialize)[¶](#gramps.gen.lib.media.Media.serialize)
Convert the data held in the event to a Python tuple that
represents all the data elements.

This method is used to convert the object into a form that can easily
be saved to a database.

These elements may be primitive Python types (string, integers),
complex Python types (lists or tuples, or Python objects. If the
target database cannot handle complex types (such as objects or
lists), the database is responsible for converting the data into
a form that it can use.

Returns
Returns a python tuple containing the data that should
be considered persistent.

Return type
tuple

`set_checksum`(*text*)[[source]](../_modules/gramps/gen/lib/media.html#Media.set_checksum)[¶](#gramps.gen.lib.media.Media.set_checksum)
Set the checksum of the image.

`set_description`(*text*)[[source]](../_modules/gramps/gen/lib/media.html#Media.set_description)[¶](#gramps.gen.lib.media.Media.set_description)
Set the description of the image.

`set_mime_type`(*mime_type*)[[source]](../_modules/gramps/gen/lib/media.html#Media.set_mime_type)[¶](#gramps.gen.lib.media.Media.set_mime_type)
Set the MIME type associated with the Media.

Parameters
**mime_type** (*str*) – MIME type to be assigned to the object

`set_path`(*path*)[[source]](../_modules/gramps/gen/lib/media.html#Media.set_path)[¶](#gramps.gen.lib.media.Media.set_path)
Set the file path to the passed path.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/media.html#Media.unserialize)[¶](#gramps.gen.lib.media.Media.unserialize)
Convert the data held in a tuple created by the serialize method
back into the data in a Media structure.

Parameters
**data** (*tuple*) – tuple containing the persistent data associated the object

### Repository[¶](#module-gramps.gen.lib.repo)
Repository object for Gramps.

*class *`gramps.gen.lib.repo.``Repository`[[source]](../_modules/gramps/gen/lib/repo.html#Repository)[¶](#gramps.gen.lib.repo.Repository)
Bases: [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.addressbase.AddressBase`](#gramps.gen.lib.addressbase.AddressBase), [`gramps.gen.lib.urlbase.UrlBase`](#gramps.gen.lib.urlbase.UrlBase), [`gramps.gen.lib.citationbase.IndirectCitationBase`](#gramps.gen.lib.citationbase.IndirectCitationBase), [`gramps.gen.lib.primaryobj.PrimaryObject`](#gramps.gen.lib.primaryobj.PrimaryObject)

A location where collections of Sources are found.

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.get_citation_child_list)[¶](#gramps.gen.lib.repo.Repository.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.get_handle_referents)[¶](#gramps.gen.lib.repo.Repository.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_name`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.get_name)[¶](#gramps.gen.lib.repo.Repository.get_name)

Returns
the descriptive name of the Repository

Return type
str

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.get_note_child_list)[¶](#gramps.gen.lib.repo.Repository.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.get_referenced_handles)[¶](#gramps.gen.lib.repo.Repository.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.get_schema)[¶](#gramps.gen.lib.repo.Repository.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.get_text_data_child_list)[¶](#gramps.gen.lib.repo.Repository.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.get_text_data_list)[¶](#gramps.gen.lib.repo.Repository.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`get_type`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.get_type)[¶](#gramps.gen.lib.repo.Repository.get_type)

Returns
the descriptive type of the Repository

Return type
str

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/repo.html#Repository.merge)[¶](#gramps.gen.lib.repo.Repository.merge)
Merge the content of acquisition into this repository.

Parameters
**acquisition** ([*Repository*](#gramps.gen.lib.repo.Repository)) – The repository to merge with the present repository.

`serialize`()[[source]](../_modules/gramps/gen/lib/repo.html#Repository.serialize)[¶](#gramps.gen.lib.repo.Repository.serialize)
Convert the object to a serialized tuple of data.

`set_name`(*name*)[[source]](../_modules/gramps/gen/lib/repo.html#Repository.set_name)[¶](#gramps.gen.lib.repo.Repository.set_name)

Parameters
**name** (*str*) – descriptive name of the Repository

`set_type`(*the_type*)[[source]](../_modules/gramps/gen/lib/repo.html#Repository.set_type)[¶](#gramps.gen.lib.repo.Repository.set_type)

Parameters
**the_type** (*str*) – descriptive type of the Repository

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/repo.html#Repository.unserialize)[¶](#gramps.gen.lib.repo.Repository.unserialize)
Convert the data held in a tuple created by the serialize method
back into the data in a Repository structure.

### Note[¶](#module-gramps.gen.lib.note)
Note class for Gramps.

*class *`gramps.gen.lib.note.``Note`(*text=''*)[[source]](../_modules/gramps/gen/lib/note.html#Note)[¶](#gramps.gen.lib.note.Note)
Bases: [`gramps.gen.lib.primaryobj.BasicPrimaryObject`](#gramps.gen.lib.primaryobj.BasicPrimaryObject)

Define a text note.

Starting from Gramps 3.1 Note object stores the text in
[`StyledText`](#gramps.gen.lib.styledtext.StyledText) instance, thus it can have text formatting
information.

To get and set only the clear text of the note use the [`get()`](#gramps.gen.lib.note.Note.get) and
[`set()`](#gramps.gen.lib.note.Note.set) methods.

To get and set the formatted version of the Note’s text use the
[`get_styledtext()`](#gramps.gen.lib.note.Note.get_styledtext) and [`set_styledtext()`](#gramps.gen.lib.note.Note.set_styledtext) methods.

The note may be ‘preformatted’ or ‘flowed’, which indicates that the
text string is considered to be in paragraphs, separated by newlines.

Variables

- [**FLOWED**](#gramps.gen.lib.note.Note.FLOWED) – indicates flowed format

- [**FORMATTED**](#gramps.gen.lib.note.Note.FORMATTED) – indicates formatted format (respecting whitespace needed)

- **POS_** – (int) Position of attribute in the serialized format of
an instance.

Warning

The POS_ class variables reflect the serialized object,
they have to be updated in case the data structure or the
[`serialize()`](#gramps.gen.lib.note.Note.serialize) method changes!

`FLOWED`* = 0*[¶](#gramps.gen.lib.note.Note.FLOWED)

`FORMATTED`* = 1*[¶](#gramps.gen.lib.note.Note.FORMATTED)

`POS_CHANGE`* = 5*[¶](#gramps.gen.lib.note.Note.POS_CHANGE)

`POS_FORMAT`* = 3*[¶](#gramps.gen.lib.note.Note.POS_FORMAT)

`POS_HANDLE`* = 0*[¶](#gramps.gen.lib.note.Note.POS_HANDLE)

`POS_ID`* = 1*[¶](#gramps.gen.lib.note.Note.POS_ID)

`POS_PRIVATE`* = 7*[¶](#gramps.gen.lib.note.Note.POS_PRIVATE)

`POS_TAGS`* = 6*[¶](#gramps.gen.lib.note.Note.POS_TAGS)

`POS_TEXT`* = 2*[¶](#gramps.gen.lib.note.Note.POS_TEXT)

`POS_TYPE`* = 4*[¶](#gramps.gen.lib.note.Note.POS_TYPE)

`append`(*text*)[[source]](../_modules/gramps/gen/lib/note.html#Note.append)[¶](#gramps.gen.lib.note.Note.append)
Append the specified text to the text associated with the note.

Parameters
**text** (str or [`StyledText`](#gramps.gen.lib.styledtext.StyledText)) – Text string to be appended to the note.

`get`()[[source]](../_modules/gramps/gen/lib/note.html#Note.get)[¶](#gramps.gen.lib.note.Note.get)
Return the text string associated with the note.

Returns
The *clear* text of the note contents.

Return type
unicode

`get_format`()[[source]](../_modules/gramps/gen/lib/note.html#Note.get_format)[¶](#gramps.gen.lib.note.Note.get_format)
Return the format of the note.

The value can either indicate Flowed or Preformatted.

Returns
0 indicates Flowed, 1 indicates Preformated

Return type
int

`get_links`()[[source]](../_modules/gramps/gen/lib/note.html#Note.get_links)[¶](#gramps.gen.lib.note.Note.get_links)
Get the jump links from this note. Links can be external, to
urls, or can be internal to gramps objects.

Return examples:

```
[("gramps", "Person", "handle", "7657626365362536"),
 ("external", "www", "url", "http://example.com")]

```

Returns
list of [(domain, type, propery, value), …]

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/note.html#Note.get_referenced_handles)[¶](#gramps.gen.lib.note.Note.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/note.html#Note.get_schema)[¶](#gramps.gen.lib.note.Note.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_styledtext`()[[source]](../_modules/gramps/gen/lib/note.html#Note.get_styledtext)[¶](#gramps.gen.lib.note.Note.get_styledtext)
Return the text string associated with the note.

Returns
The *formatted* text of the note contents.

Return type
[`StyledText`](#gramps.gen.lib.styledtext.StyledText)

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/note.html#Note.get_text_data_list)[¶](#gramps.gen.lib.note.Note.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
The list of all textual attributes of the object.

Return type
list

`get_type`()[[source]](../_modules/gramps/gen/lib/note.html#Note.get_type)[¶](#gramps.gen.lib.note.Note.get_type)
Get descriptive type of the Note.

Returns
the descriptive type of the Note

Return type
str

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/note.html#Note.merge)[¶](#gramps.gen.lib.note.Note.merge)
Merge the content of acquisition into this note.

Lost: handle, id, type, format, text and styles of acquisition.

Parameters
**acquisition** ([*Note*](#gramps.gen.lib.note.Note)) – The note to merge with the present note.

`serialize`()[[source]](../_modules/gramps/gen/lib/note.html#Note.serialize)[¶](#gramps.gen.lib.note.Note.serialize)
Convert the object to a serialized tuple of data.

Returns
The serialized format of the instance.

Return type
tuple

`set`(*text*)[[source]](../_modules/gramps/gen/lib/note.html#Note.set)[¶](#gramps.gen.lib.note.Note.set)
Set the text associated with the note to the passed string.

Parameters
**text** (*str*) – The *clear* text defining the note contents.

`set_format`(*format*)[[source]](../_modules/gramps/gen/lib/note.html#Note.set_format)[¶](#gramps.gen.lib.note.Note.set_format)
Set the format of the note to the passed value.

Parameters
**format** (*int*) – The value can either indicate Flowed or Preformatted.

`set_styledtext`(*text*)[[source]](../_modules/gramps/gen/lib/note.html#Note.set_styledtext)[¶](#gramps.gen.lib.note.Note.set_styledtext)
Set the text associated with the note to the passed string.

Parameters
**text** ([`StyledText`](#gramps.gen.lib.styledtext.StyledText)) – The *formatted* text defining the note contents.

`set_type`(*the_type*)[[source]](../_modules/gramps/gen/lib/note.html#Note.set_type)[¶](#gramps.gen.lib.note.Note.set_type)
Set descriptive type of the Note.

Parameters
**the_type** (*str*) – descriptive type of the Note

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/note.html#Note.unserialize)[¶](#gramps.gen.lib.note.Note.unserialize)
Convert a serialized tuple of data to an object.

Parameters
**data** – The serialized format of a Note.

Type
data: tuple

## Secondary objects[¶](#secondary-objects)

### Secondary Object[¶](#module-gramps.gen.lib.secondaryobj)
Secondary Object class for Gramps.

*class *`gramps.gen.lib.secondaryobj.``SecondaryObject`[[source]](../_modules/gramps/gen/lib/secondaryobj.html#SecondaryObject)[¶](#gramps.gen.lib.secondaryobj.SecondaryObject)
Bases: [`gramps.gen.lib.baseobj.BaseObject`](#gramps.gen.lib.baseobj.BaseObject)

The SecondaryObject is the base class for all secondary objects in the
database.

`is_equal`(*source*)[[source]](../_modules/gramps/gen/lib/secondaryobj.html#SecondaryObject.is_equal)[¶](#gramps.gen.lib.secondaryobj.SecondaryObject.is_equal)

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/secondaryobj.html#SecondaryObject.is_equivalent)[¶](#gramps.gen.lib.secondaryobj.SecondaryObject.is_equivalent)
Return if this object is equivalent to other.

Should be overwritten by objects that inherit from this class.

`serialize`()[[source]](../_modules/gramps/gen/lib/secondaryobj.html#SecondaryObject.serialize)[¶](#gramps.gen.lib.secondaryobj.SecondaryObject.serialize)
Convert the object to a serialized tuple of data.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/secondaryobj.html#SecondaryObject.unserialize)[¶](#gramps.gen.lib.secondaryobj.SecondaryObject.unserialize)
Convert a serialized tuple of data to an object.

### Address[¶](#module-gramps.gen.lib.address)
Address class for Gramps.

*class *`gramps.gen.lib.address.``Address`(*source=None*)[[source]](../_modules/gramps/gen/lib/address.html#Address)[¶](#gramps.gen.lib.address.Address)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase), [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.datebase.DateBase`](#gramps.gen.lib.datebase.DateBase), [`gramps.gen.lib.locationbase.LocationBase`](#gramps.gen.lib.locationbase.LocationBase)

Provide address information.

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/address.html#Address.get_handle_referents)[¶](#gramps.gen.lib.address.Address.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/address.html#Address.get_note_child_list)[¶](#gramps.gen.lib.address.Address.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/address.html#Address.get_referenced_handles)[¶](#gramps.gen.lib.address.Address.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/address.html#Address.get_schema)[¶](#gramps.gen.lib.address.Address.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/address.html#Address.get_text_data_child_list)[¶](#gramps.gen.lib.address.Address.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/address.html#Address.get_text_data_list)[¶](#gramps.gen.lib.address.Address.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/address.html#Address.is_equivalent)[¶](#gramps.gen.lib.address.Address.is_equivalent)
Return if this address is equivalent, that is agrees in location and
date, to other.

Parameters
**other** ([*Address*](#gramps.gen.lib.address.Address)) – The address to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/address.html#Address.merge)[¶](#gramps.gen.lib.address.Address.merge)
Merge the content of acquisition into this address.

Lost: date, street, city, county, state, country, postal and phone of
acquisition.

Parameters
**acquisition** ([*Address*](#gramps.gen.lib.address.Address)) – The address to merge with the present address.

`serialize`()[[source]](../_modules/gramps/gen/lib/address.html#Address.serialize)[¶](#gramps.gen.lib.address.Address.serialize)
Convert the object to a serialized tuple of data.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/address.html#Address.unserialize)[¶](#gramps.gen.lib.address.Address.unserialize)
Convert a serialized tuple of data to an object.

### Attribute[¶](#module-gramps.gen.lib.attribute)
Attribute class for Gramps.

*class *`gramps.gen.lib.attribute.``Attribute`(*source=None*)[[source]](../_modules/gramps/gen/lib/attribute.html#Attribute)[¶](#gramps.gen.lib.attribute.Attribute)
Bases: [`gramps.gen.lib.attribute.AttributeRoot`](#gramps.gen.lib.attribute.AttributeRoot), [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase)

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/attribute.html#Attribute.get_referenced_handles)[¶](#gramps.gen.lib.attribute.Attribute.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/attribute.html#Attribute.get_schema)[¶](#gramps.gen.lib.attribute.Attribute.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/attribute.html#Attribute.merge)[¶](#gramps.gen.lib.attribute.Attribute.merge)
Merge the content of acquisition into this attribute.

Lost: type and value of acquisition.

Parameters
**acquisition** ([*Attribute*](#gramps.gen.lib.attribute.Attribute)) – the attribute to merge with the present attribute.

`serialize`()[[source]](../_modules/gramps/gen/lib/attribute.html#Attribute.serialize)[¶](#gramps.gen.lib.attribute.Attribute.serialize)
Convert the object to a serialized tuple of data.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/attribute.html#Attribute.unserialize)[¶](#gramps.gen.lib.attribute.Attribute.unserialize)
Convert a serialized tuple of data to an object.

### AttributeRoot[¶](#attributeroot)

*class *`gramps.gen.lib.attribute.``AttributeRoot`(*source=None*)[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot)[¶](#gramps.gen.lib.attribute.AttributeRoot)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase)

Provide a simple key/value pair for describing properties.
Used to store descriptive information.

In GEDCOM only used for Persons:
Individual attributes should describe situations that may be permanent or
temporary (start at some date, end at some date, etc.), may be associated
to a place (a position held, residence, etc.) or may not (eye colour,
height, caste, profession, etc.). They may have sources and notes and
media.
Compare with [`Event`](#gramps.gen.lib.event.Event)

Gramps at the moment does not support this GEDCOM Attribute structure.

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.get_handle_referents)[¶](#gramps.gen.lib.attribute.AttributeRoot.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.get_note_child_list)[¶](#gramps.gen.lib.attribute.AttributeRoot.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.get_referenced_handles)[¶](#gramps.gen.lib.attribute.AttributeRoot.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.get_text_data_child_list)[¶](#gramps.gen.lib.attribute.AttributeRoot.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.get_text_data_list)[¶](#gramps.gen.lib.attribute.AttributeRoot.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`get_type`()[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.get_type)[¶](#gramps.gen.lib.attribute.AttributeRoot.get_type)
Return the type (or key) or the Attribute instance.

`get_value`()[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.get_value)[¶](#gramps.gen.lib.attribute.AttributeRoot.get_value)
Return the value of the Attribute instance.

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.is_equivalent)[¶](#gramps.gen.lib.attribute.AttributeRoot.is_equivalent)
Return if this attribute is equivalent, that is agrees in type and
value, to other.

Parameters
**other** ([*Attribute*](#gramps.gen.lib.attribute.Attribute)) – The attribute to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.merge)[¶](#gramps.gen.lib.attribute.AttributeRoot.merge)
Merge the content of acquisition into this attribute.

Lost: type and value of acquisition.

Parameters
**acquisition** ([*Attribute*](#gramps.gen.lib.attribute.Attribute)) – the attribute to merge with the present attribute.

`serialize`()[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.serialize)[¶](#gramps.gen.lib.attribute.AttributeRoot.serialize)
Convert the object to a serialized tuple of data.

`set_type`(*val*)[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.set_type)[¶](#gramps.gen.lib.attribute.AttributeRoot.set_type)
Set the type (or key) of the Attribute instance.

`set_value`(*val*)[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.set_value)[¶](#gramps.gen.lib.attribute.AttributeRoot.set_value)
Set the value of the Attribute instance.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/attribute.html#AttributeRoot.unserialize)[¶](#gramps.gen.lib.attribute.AttributeRoot.unserialize)
Convert a serialized tuple of data to an object.

### LdsOrd[¶](#module-gramps.gen.lib.ldsord)
LDS Ordinance class for Gramps.

*class *`gramps.gen.lib.ldsord.``LdsOrd`(*source=None*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd)[¶](#gramps.gen.lib.ldsord.LdsOrd)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.datebase.DateBase`](#gramps.gen.lib.datebase.DateBase), [`gramps.gen.lib.placebase.PlaceBase`](#gramps.gen.lib.placebase.PlaceBase), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase)

Class that contains information about LDS Ordinances.

LDS ordinances are similar to events, but have very specific additional
information related to data collected by the Church of Jesus Christ
of Latter Day Saints (Mormon church). The LDS church is the largest
source of genealogical information in the United States.

`BAPTISM`* = 0*[¶](#gramps.gen.lib.ldsord.LdsOrd.BAPTISM)

`CONFIRMATION`* = 4*[¶](#gramps.gen.lib.ldsord.LdsOrd.CONFIRMATION)

`DEFAULT_STATUS`* = 0*[¶](#gramps.gen.lib.ldsord.LdsOrd.DEFAULT_STATUS)

`DEFAULT_TYPE`* = 0*[¶](#gramps.gen.lib.ldsord.LdsOrd.DEFAULT_TYPE)

`ENDOWMENT`* = 1*[¶](#gramps.gen.lib.ldsord.LdsOrd.ENDOWMENT)

`SEAL_TO_PARENTS`* = 2*[¶](#gramps.gen.lib.ldsord.LdsOrd.SEAL_TO_PARENTS)

`SEAL_TO_SPOUSE`* = 3*[¶](#gramps.gen.lib.ldsord.LdsOrd.SEAL_TO_SPOUSE)

`STATUS_BIC`* = 1*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_BIC)

`STATUS_CANCELED`* = 2*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_CANCELED)

`STATUS_CHILD`* = 3*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_CHILD)

`STATUS_CLEARED`* = 4*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_CLEARED)

`STATUS_COMPLETED`* = 5*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_COMPLETED)

`STATUS_DNS`* = 6*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_DNS)

`STATUS_DNS_CAN`* = 10*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_DNS_CAN)

`STATUS_INFANT`* = 7*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_INFANT)

`STATUS_NONE`* = 0*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_NONE)

`STATUS_PRE_1970`* = 8*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_PRE_1970)

`STATUS_QUALIFIED`* = 9*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_QUALIFIED)

`STATUS_STILLBORN`* = 11*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_STILLBORN)

`STATUS_SUBMITTED`* = 12*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_SUBMITTED)

`STATUS_UNCLEARED`* = 13*[¶](#gramps.gen.lib.ldsord.LdsOrd.STATUS_UNCLEARED)

`are_equal`(*other*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.are_equal)[¶](#gramps.gen.lib.ldsord.LdsOrd.are_equal)
Return 1 if the specified ordinance is the same as the instance.

`get_family_handle`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_family_handle)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_family_handle)
Get the Family database handle associated with the LDS ordinance.

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_handle_referents)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_note_child_list)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_referenced_handles)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_schema)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_status`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_status)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_status)
Get the status of the LDS ordinance.

`get_temple`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_temple)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_temple)
Get the temple associated with the ordinance.

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_text_data_child_list)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_text_data_list)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`get_type`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.get_type)[¶](#gramps.gen.lib.ldsord.LdsOrd.get_type)
Return the type of the Event.

Returns
Type of the Event

Return type
tuple

`is_empty`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.is_empty)[¶](#gramps.gen.lib.ldsord.LdsOrd.is_empty)
Return 1 if the ordinance is actually empty.

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.is_equivalent)[¶](#gramps.gen.lib.ldsord.LdsOrd.is_equivalent)
Return if this ldsord is equivalent, that is agrees in date, temple,
place, status, sealed_to, to other.

Parameters
**other** ([*LdsOrd*](#gramps.gen.lib.ldsord.LdsOrd)) – The ldsord to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.merge)[¶](#gramps.gen.lib.ldsord.LdsOrd.merge)
Merge the content of acquisition into this ldsord.

Lost: type, date, temple, place, status, sealed_to of acquistion.

Parameters
**acquisition** ([*LdsOrd*](#gramps.gen.lib.ldsord.LdsOrd)) – The ldsord to merge with the present ldsord.

`serialize`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.serialize)[¶](#gramps.gen.lib.ldsord.LdsOrd.serialize)
Convert the object to a serialized tuple of data.

`set_family_handle`(*family*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.set_family_handle)[¶](#gramps.gen.lib.ldsord.LdsOrd.set_family_handle)
Set the Family database handle associated with the LDS ordinance.

`set_status`(*val*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.set_status)[¶](#gramps.gen.lib.ldsord.LdsOrd.set_status)
Set the status of the LDS ordinance.

The status is a text string that matches a predefined set of strings.

`set_status_from_xml`(*xml_str*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.set_status_from_xml)[¶](#gramps.gen.lib.ldsord.LdsOrd.set_status_from_xml)
Set status based on a given string from XML.

Return boolean on success.

`set_temple`(*temple*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.set_temple)[¶](#gramps.gen.lib.ldsord.LdsOrd.set_temple)
Set the temple associated with the ordinance.

`set_type`(*ord_type*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.set_type)[¶](#gramps.gen.lib.ldsord.LdsOrd.set_type)
Set the type of the LdsOrd to the passed (int,str) tuple.

Parameters
**ord_type** (*tuple*) – Type to assign to the LdsOrd

`set_type_from_xml`(*xml_str*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.set_type_from_xml)[¶](#gramps.gen.lib.ldsord.LdsOrd.set_type_from_xml)
Set type based on a given string from XML.

Return boolean on success.

`status2str`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.status2str)[¶](#gramps.gen.lib.ldsord.LdsOrd.status2str)
Return status-representing string suitable for UI (translated).

`status2xml`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.status2xml)[¶](#gramps.gen.lib.ldsord.LdsOrd.status2xml)
Return status-representing string suitable for XML.

`type2str`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.type2str)[¶](#gramps.gen.lib.ldsord.LdsOrd.type2str)
Return type-representing string suitable for UI (translated).

`type2xml`()[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.type2xml)[¶](#gramps.gen.lib.ldsord.LdsOrd.type2xml)
Return type-representing string suitable for XML.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/ldsord.html#LdsOrd.unserialize)[¶](#gramps.gen.lib.ldsord.LdsOrd.unserialize)
Convert a serialized tuple of data to an object.

### Location[¶](#module-gramps.gen.lib.location)
Location class for Gramps.

*class *`gramps.gen.lib.location.``Location`(*source=None*)[[source]](../_modules/gramps/gen/lib/location.html#Location)[¶](#gramps.gen.lib.location.Location)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.locationbase.LocationBase`](#gramps.gen.lib.locationbase.LocationBase)

Provide information about a place.

The data including street, locality, city, county, state, and country.
Multiple Location objects can represent the same place, since names
of cities, counties, states, and even countries can change with time.

`get_parish`()[[source]](../_modules/gramps/gen/lib/location.html#Location.get_parish)[¶](#gramps.gen.lib.location.Location.get_parish)
Get the religious parish name.

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/location.html#Location.get_schema)[¶](#gramps.gen.lib.location.Location.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/location.html#Location.get_text_data_list)[¶](#gramps.gen.lib.location.Location.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`is_empty`()[[source]](../_modules/gramps/gen/lib/location.html#Location.is_empty)[¶](#gramps.gen.lib.location.Location.is_empty)

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/location.html#Location.is_equivalent)[¶](#gramps.gen.lib.location.Location.is_equivalent)
Return if this location is equivalent to other.

Parameters
**other** ([*Location*](#gramps.gen.lib.location.Location)) – The location to compare this one to.

Returns
Constant inidicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/location.html#Location.merge)[¶](#gramps.gen.lib.location.Location.merge)
Merge the content of acquisition into this location.

Lost: everything of acquisition.

Parameters
**acquisition** ([*Location*](#gramps.gen.lib.location.Location)) – The location to merge with the present location.

`serialize`()[[source]](../_modules/gramps/gen/lib/location.html#Location.serialize)[¶](#gramps.gen.lib.location.Location.serialize)
Convert the object to a serialized tuple of data.

`set_parish`(*data*)[[source]](../_modules/gramps/gen/lib/location.html#Location.set_parish)[¶](#gramps.gen.lib.location.Location.set_parish)
Set the religious parish name.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/location.html#Location.unserialize)[¶](#gramps.gen.lib.location.Location.unserialize)
Convert a serialized tuple of data to an object.

### Name[¶](#module-gramps.gen.lib.name)
Name class for Gramps.

*class *`gramps.gen.lib.name.``Name`(*source=None*, *data=None*)[[source]](../_modules/gramps/gen/lib/name.html#Name)[¶](#gramps.gen.lib.name.Name)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase), [`gramps.gen.lib.surnamebase.SurnameBase`](#gramps.gen.lib.surnamebase.SurnameBase), [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.datebase.DateBase`](#gramps.gen.lib.datebase.DateBase)

Provide name information about a person.

A person may have more that one name throughout his or her life. The Name
object stores one of them

`DEF`* = 0*[¶](#gramps.gen.lib.name.Name.DEF)

`FN`* = 4*[¶](#gramps.gen.lib.name.Name.FN)

`FNLN`* = 2*[¶](#gramps.gen.lib.name.Name.FNLN)

`LNFN`* = 1*[¶](#gramps.gen.lib.name.Name.LNFN)

`LNFNP`* = 5*[¶](#gramps.gen.lib.name.Name.LNFNP)

`NAMEFORMATS`* = (0, 1, 2, 4, 5)*[¶](#gramps.gen.lib.name.Name.NAMEFORMATS)

`PTFN`* = 3*[¶](#gramps.gen.lib.name.Name.PTFN)

`get_call_name`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_call_name)[¶](#gramps.gen.lib.name.Name.get_call_name)
Return the call name.

The call name’s exact definition is not predetermined, and may be
locale specific.

`get_display_as`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_display_as)[¶](#gramps.gen.lib.name.Name.get_display_as)
Return the selected display format for the name.

The options are LNFN (last name, first name), FNLN (first name, last
name), etc.

`get_family_nick_name`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_family_nick_name)[¶](#gramps.gen.lib.name.Name.get_family_nick_name)
Return the family nick name.

The family nick name of the family of the person, a not official name
use to denote the entire family.

`get_first_name`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_first_name)[¶](#gramps.gen.lib.name.Name.get_first_name)
Return the given name for the Name instance.

`get_gedcom_name`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_gedcom_name)[¶](#gramps.gen.lib.name.Name.get_gedcom_name)
Returns a GEDCOM-formatted name.

`get_gedcom_parts`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_gedcom_parts)[¶](#gramps.gen.lib.name.Name.get_gedcom_parts)
Returns a GEDCOM-formatted name dictionary.

Note

Fields patronymic and prefix are deprecated, prefix_list and
surname list, added.

`get_group_as`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_group_as)[¶](#gramps.gen.lib.name.Name.get_group_as)
Return the grouping name, which is used to group equivalent surnames.

`get_group_name`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_group_name)[¶](#gramps.gen.lib.name.Name.get_group_name)
Return the grouping name, which is used to group equivalent surnames.

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_handle_referents)[¶](#gramps.gen.lib.name.Name.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_name`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_name)[¶](#gramps.gen.lib.name.Name.get_name)
Return a name string built from the components of the Name instance,
in the form of: surname, Firstname.

`get_nick_name`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_nick_name)[¶](#gramps.gen.lib.name.Name.get_nick_name)
Return the nick name.

The nick name of the person, a not official name the person is known
with.

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_note_child_list)[¶](#gramps.gen.lib.name.Name.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_referenced_handles)[¶](#gramps.gen.lib.name.Name.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

`get_regular_name`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_regular_name)[¶](#gramps.gen.lib.name.Name.get_regular_name)
Return a name string built from the components of the Name instance,
in the form of Firstname surname.

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_schema)[¶](#gramps.gen.lib.name.Name.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_sort_as`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_sort_as)[¶](#gramps.gen.lib.name.Name.get_sort_as)
Return the selected sorting method for the name.

The options are LNFN (last name, first name), FNLN (first name, last
name), etc.

`get_suffix`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_suffix)[¶](#gramps.gen.lib.name.Name.get_suffix)
Return the suffix for the Name instance.

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_text_data_child_list)[¶](#gramps.gen.lib.name.Name.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_text_data_list)[¶](#gramps.gen.lib.name.Name.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`get_title`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_title)[¶](#gramps.gen.lib.name.Name.get_title)
Return the title for the Name instance.

`get_type`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_type)[¶](#gramps.gen.lib.name.Name.get_type)
Return the type of the Name instance.

`get_upper_name`()[[source]](../_modules/gramps/gen/lib/name.html#Name.get_upper_name)[¶](#gramps.gen.lib.name.Name.get_upper_name)
Return a name string built from the components of the Name instance,
in the form of SURNAME, Firstname.

`is_empty`()[[source]](../_modules/gramps/gen/lib/name.html#Name.is_empty)[¶](#gramps.gen.lib.name.Name.is_empty)
Indicate if the name is empty.

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/name.html#Name.is_equivalent)[¶](#gramps.gen.lib.name.Name.is_equivalent)
Return if this name is equivalent, that is agrees in type, first,
call, surname_list, suffix, title and date, to other.

Parameters
**other** ([*Name*](#gramps.gen.lib.name.Name)) – The name to compare this name to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/name.html#Name.merge)[¶](#gramps.gen.lib.name.Name.merge)
Merge the content of acquisition into this name.
Normally the person merge code should opt for adding an alternate
name if names are actually different (like not equal surname list)

Lost: type, first, call, suffix, title, nick, famnick and date of
acquisition.

Parameters
**acquisition** ([*Name*](#gramps.gen.lib.name.Name)) – The name to merge with the present name.

`serialize`()[[source]](../_modules/gramps/gen/lib/name.html#Name.serialize)[¶](#gramps.gen.lib.name.Name.serialize)
Convert the object to a serialized tuple of data.

`set_call_name`(*val*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_call_name)[¶](#gramps.gen.lib.name.Name.set_call_name)
Set the call name.

The call name’s exact definition is not predetermined, and may be
locale specific.

`set_display_as`(*value*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_display_as)[¶](#gramps.gen.lib.name.Name.set_display_as)
Specifies the display format for the specified name.

Typically the locale’s default should be used. However, there may be
names where a specific display format is desired for a name.

`set_family_nick_name`(*val*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_family_nick_name)[¶](#gramps.gen.lib.name.Name.set_family_nick_name)
Set the family nick name.

The family nick name of the family of the person, a not official name
use to denote the entire family.

`set_first_name`(*name*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_first_name)[¶](#gramps.gen.lib.name.Name.set_first_name)
Set the given name for the Name instance.

`set_group_as`(*name*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_group_as)[¶](#gramps.gen.lib.name.Name.set_group_as)
Set the grouping name for a person.

Normally, this is the person’s surname. However, some locales group
equivalent names (e.g. Ivanova and Ivanov in Russian are usually
considered equivalent.

Note

There is also a database wide grouping set_name_group_mapping
So one might map a name Smith to SmithNew, and have one person still
grouped with name Smith. Hence, group_as can be equal to surname!

`set_nick_name`(*val*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_nick_name)[¶](#gramps.gen.lib.name.Name.set_nick_name)
Set the nick name.

The nick name of the person, a not official name the person is known
with.

`set_sort_as`(*value*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_sort_as)[¶](#gramps.gen.lib.name.Name.set_sort_as)
Specifies the sorting method for the specified name.

Typically the locale’s default should be used. However, there may be
names where a specific sorting structure is desired for a name.

`set_suffix`(*name*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_suffix)[¶](#gramps.gen.lib.name.Name.set_suffix)
Set the suffix (such as Jr., III, etc.) for the Name instance.

`set_title`(*title*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_title)[¶](#gramps.gen.lib.name.Name.set_title)
Set the title (Dr., Reverand, Captain) for the Name instance.

`set_type`(*the_type*)[[source]](../_modules/gramps/gen/lib/name.html#Name.set_type)[¶](#gramps.gen.lib.name.Name.set_type)
Set the type of the Name instance.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/name.html#Name.unserialize)[¶](#gramps.gen.lib.name.Name.unserialize)
Convert a serialized tuple of data to an object.

### Surname[¶](#module-gramps.gen.lib.surname)
Surname class for Gramps.

*class *`gramps.gen.lib.surname.``Surname`(*source=None*, *data=None*)[[source]](../_modules/gramps/gen/lib/surname.html#Surname)[¶](#gramps.gen.lib.surname.Surname)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject)

Provide surname information of a name.

A person may have more that one surname in his name

`get_connector`()[[source]](../_modules/gramps/gen/lib/surname.html#Surname.get_connector)[¶](#gramps.gen.lib.surname.Surname.get_connector)
Get the connector for the Surname instance. This defines how a
surname connects to the next surname (eg in Spanish names).

`get_origintype`()[[source]](../_modules/gramps/gen/lib/surname.html#Surname.get_origintype)[¶](#gramps.gen.lib.surname.Surname.get_origintype)
Return the origin type of the Surname instance.

`get_prefix`()[[source]](../_modules/gramps/gen/lib/surname.html#Surname.get_prefix)[¶](#gramps.gen.lib.surname.Surname.get_prefix)
Return the prefix (or article) of the surname.

The prefix is not used for sorting or grouping.

`get_primary`()[[source]](../_modules/gramps/gen/lib/surname.html#Surname.get_primary)[¶](#gramps.gen.lib.surname.Surname.get_primary)
Return if this surname is the primary surname

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/surname.html#Surname.get_schema)[¶](#gramps.gen.lib.surname.Surname.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_surname`()[[source]](../_modules/gramps/gen/lib/surname.html#Surname.get_surname)[¶](#gramps.gen.lib.surname.Surname.get_surname)
Return the surname.

The surname is one of the not given names coming from the parents

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/surname.html#Surname.get_text_data_list)[¶](#gramps.gen.lib.surname.Surname.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`is_empty`()[[source]](../_modules/gramps/gen/lib/surname.html#Surname.is_empty)[¶](#gramps.gen.lib.surname.Surname.is_empty)
Indicate if the surname is empty.

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/surname.html#Surname.is_equivalent)[¶](#gramps.gen.lib.surname.Surname.is_equivalent)
Return if this surname is equivalent, that is agrees in type, surname,
…, to other.

Parameters
**other** ([*Surname*](#gramps.gen.lib.surname.Surname)) – The surname to compare this name to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/surname.html#Surname.merge)[¶](#gramps.gen.lib.surname.Surname.merge)
Merge the content of acquisition into this surname.

Lost: primary, surname, prefix, connector, origintype

Parameters
**acquisition** ([*Surname*](#gramps.gen.lib.surname.Surname)) – The surname to merge with the present surname.

`serialize`()[[source]](../_modules/gramps/gen/lib/surname.html#Surname.serialize)[¶](#gramps.gen.lib.surname.Surname.serialize)
Convert the object to a serialized tuple of data.

`set_connector`(*connector*)[[source]](../_modules/gramps/gen/lib/surname.html#Surname.set_connector)[¶](#gramps.gen.lib.surname.Surname.set_connector)
Set the connector for the Surname instance. This defines how a
surname connects to the next surname (eg in Spanish names).

`set_origintype`(*the_type*)[[source]](../_modules/gramps/gen/lib/surname.html#Surname.set_origintype)[¶](#gramps.gen.lib.surname.Surname.set_origintype)
Set the origin type of the Surname instance.

`set_prefix`(*val*)[[source]](../_modules/gramps/gen/lib/surname.html#Surname.set_prefix)[¶](#gramps.gen.lib.surname.Surname.set_prefix)
Set the prefix (or article) of the surname.

Examples of articles would be ‘de’ or ‘van’.

`set_primary`(*primary=True*)[[source]](../_modules/gramps/gen/lib/surname.html#Surname.set_primary)[¶](#gramps.gen.lib.surname.Surname.set_primary)
Set if this surname is the primary surname.replace
Use [`SurnameBase`](#gramps.gen.lib.surnamebase.SurnameBase) to set the primary surname
via [`set_primary_surname()`](#gramps.gen.lib.surnamebase.SurnameBase.set_primary_surname)

Parameters
**primary** (*bool*) – primay surname or not

`set_surname`(*val*)[[source]](../_modules/gramps/gen/lib/surname.html#Surname.set_surname)[¶](#gramps.gen.lib.surname.Surname.set_surname)
Set the surname.

The surname is one of the not given names coming from the parents

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/surname.html#Surname.unserialize)[¶](#gramps.gen.lib.surname.Surname.unserialize)
Convert a serialized tuple of data to an object.

### Url[¶](#module-gramps.gen.lib.url)
Url class for Gramps.

*class *`gramps.gen.lib.url.``Url`(*source=None*)[[source]](../_modules/gramps/gen/lib/url.html#Url)[¶](#gramps.gen.lib.url.Url)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase)

Contains information related to internet Uniform Resource Locators,
allowing gramps to store information about internet resources.

`are_equal`(*other*)[[source]](../_modules/gramps/gen/lib/url.html#Url.are_equal)[¶](#gramps.gen.lib.url.Url.are_equal)
Deprecated - use [`is_equal()`](#gramps.gen.lib.secondaryobj.SecondaryObject.is_equal) instead.

`get_description`()[[source]](../_modules/gramps/gen/lib/url.html#Url.get_description)[¶](#gramps.gen.lib.url.Url.get_description)
Return the description of the URL.

`get_full_path`()[[source]](../_modules/gramps/gen/lib/url.html#Url.get_full_path)[¶](#gramps.gen.lib.url.Url.get_full_path)
Returns a full url, complete with scheme, even if missing from path.

`get_path`()[[source]](../_modules/gramps/gen/lib/url.html#Url.get_path)[¶](#gramps.gen.lib.url.Url.get_path)
Return the URL path.

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/url.html#Url.get_schema)[¶](#gramps.gen.lib.url.Url.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/url.html#Url.get_text_data_list)[¶](#gramps.gen.lib.url.Url.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`get_type`()[[source]](../_modules/gramps/gen/lib/url.html#Url.get_type)[¶](#gramps.gen.lib.url.Url.get_type)

Returns
the descriptive type of the Url

Return type
str

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/url.html#Url.is_equivalent)[¶](#gramps.gen.lib.url.Url.is_equivalent)
Return if this url is equivalent, that is agrees in type, full path
name and description, to other.

Parameters
**other** ([*Url*](#gramps.gen.lib.url.Url)) – The url to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/url.html#Url.merge)[¶](#gramps.gen.lib.url.Url.merge)
Merge the content of acquisition into this url.

Parameters
**acquisition** ([*Url*](#gramps.gen.lib.url.Url)) – The url to merge with the present url.

`parse_path`()[[source]](../_modules/gramps/gen/lib/url.html#Url.parse_path)[¶](#gramps.gen.lib.url.Url.parse_path)
Returns a 6 tuple-based object with the following items:

| Table |
|-------|

| Property

 |
Pos

 |
Meaning

 |
 |

| scheme

 |
0

 |
URL scheme specifier

 |
 |
| netloc

 |
1

 |
Network location part

 |
 |
| path

 |
2

 |
Hierarchical path

 |
 |
| params

 |
3

 |
Parameters for last path element

 |
 |
| query

 |
4

 |
Query component

 |
 |
| fragment

 |
5

 |
Fragment identifier

 |
 |

`serialize`()[[source]](../_modules/gramps/gen/lib/url.html#Url.serialize)[¶](#gramps.gen.lib.url.Url.serialize)
Convert the object to a serialized tuple of data.

`set_description`(*description*)[[source]](../_modules/gramps/gen/lib/url.html#Url.set_description)[¶](#gramps.gen.lib.url.Url.set_description)
Set the description of the URL.

`set_path`(*path*)[[source]](../_modules/gramps/gen/lib/url.html#Url.set_path)[¶](#gramps.gen.lib.url.Url.set_path)
Set the URL path.

`set_type`(*the_type*)[[source]](../_modules/gramps/gen/lib/url.html#Url.set_type)[¶](#gramps.gen.lib.url.Url.set_type)

Parameters
**the_type** (*str*) – descriptive type of the Url

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/url.html#Url.unserialize)[¶](#gramps.gen.lib.url.Url.unserialize)
Convert a serialized tuple of data to an object.

## Reference objects[¶](#reference-objects)

### ChildRef[¶](#module-gramps.gen.lib.childref)
Child Reference class for Gramps.

*class *`gramps.gen.lib.childref.``ChildRef`(*source=None*)[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef)[¶](#gramps.gen.lib.childref.ChildRef)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase), [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.refbase.RefBase`](#gramps.gen.lib.refbase.RefBase)

Person reference class.

This class is for keeping information about how the person relates
to another person from the database, if not through family.
Examples would be: godparent, friend, etc.

`get_father_relation`()[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.get_father_relation)[¶](#gramps.gen.lib.childref.ChildRef.get_father_relation)
Return the relation between the person and father.

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.get_handle_referents)[¶](#gramps.gen.lib.childref.ChildRef.get_handle_referents)
Return the list of child objects which may, directly or through their
children, reference primary objects..

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_mother_relation`()[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.get_mother_relation)[¶](#gramps.gen.lib.childref.ChildRef.get_mother_relation)
Return the relation between the person and mother.

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.get_note_child_list)[¶](#gramps.gen.lib.childref.ChildRef.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.get_referenced_handles)[¶](#gramps.gen.lib.childref.ChildRef.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.get_schema)[¶](#gramps.gen.lib.childref.ChildRef.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.get_text_data_child_list)[¶](#gramps.gen.lib.childref.ChildRef.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.get_text_data_list)[¶](#gramps.gen.lib.childref.ChildRef.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.is_equivalent)[¶](#gramps.gen.lib.childref.ChildRef.is_equivalent)
Return if this child reference is equivalent, that is agrees in hlink,
to other.

Parameters
**other** ([*ChildRef*](#gramps.gen.lib.childref.ChildRef)) – The childref to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.merge)[¶](#gramps.gen.lib.childref.ChildRef.merge)
Merge the content of acquisition into this child reference.

Lost: hlink, mrel and frel of acquisition.

Parameters
**acquisition** ([*ChildRef*](#gramps.gen.lib.childref.ChildRef)) – The childref to merge with the present childref.

`serialize`()[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.serialize)[¶](#gramps.gen.lib.childref.ChildRef.serialize)
Convert the object to a serialized tuple of data.

`set_father_relation`(*frel*)[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.set_father_relation)[¶](#gramps.gen.lib.childref.ChildRef.set_father_relation)
Set relation between the person and father.

`set_mother_relation`(*rel*)[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.set_mother_relation)[¶](#gramps.gen.lib.childref.ChildRef.set_mother_relation)
Set relation between the person and mother.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/childref.html#ChildRef.unserialize)[¶](#gramps.gen.lib.childref.ChildRef.unserialize)
Convert a serialized tuple of data to an object.

### EventRef[¶](#module-gramps.gen.lib.eventref)
Event Reference class for Gramps

*class *`gramps.gen.lib.eventref.``EventRef`(*source=None*)[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef)[¶](#gramps.gen.lib.eventref.EventRef)
Bases: [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.attrbase.AttributeBase`](#gramps.gen.lib.attrbase.AttributeBase), [`gramps.gen.lib.refbase.RefBase`](#gramps.gen.lib.refbase.RefBase), [`gramps.gen.lib.citationbase.IndirectCitationBase`](#gramps.gen.lib.citationbase.IndirectCitationBase), [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject)

Event reference class.

This class is for keeping information about how the person relates
to the referenced event.

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.get_citation_child_list)[¶](#gramps.gen.lib.eventref.EventRef.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.get_handle_referents)[¶](#gramps.gen.lib.eventref.EventRef.get_handle_referents)
Return the list of child objects which may, directly or through their
children, reference primary objects..

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.get_note_child_list)[¶](#gramps.gen.lib.eventref.EventRef.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.get_referenced_handles)[¶](#gramps.gen.lib.eventref.EventRef.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
Returns the list of (classname, handle) tuples for referenced
objects.

Return type
list

`get_role`()[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.get_role)[¶](#gramps.gen.lib.eventref.EventRef.get_role)
Return the tuple corresponding to the preset role.

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.get_schema)[¶](#gramps.gen.lib.eventref.EventRef.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.get_text_data_child_list)[¶](#gramps.gen.lib.eventref.EventRef.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.get_text_data_list)[¶](#gramps.gen.lib.eventref.EventRef.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.is_equivalent)[¶](#gramps.gen.lib.eventref.EventRef.is_equivalent)
Return if this eventref is equivalent, that is agrees in handle and
role, to other.

Parameters
**other** ([*EventRef*](#gramps.gen.lib.eventref.EventRef)) – The eventref to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.merge)[¶](#gramps.gen.lib.eventref.EventRef.merge)
Merge the content of acquisition into this eventref.

Lost: hlink and role of acquisition.

Parameters
**acquisition** ([*EventRef*](#gramps.gen.lib.eventref.EventRef)) – The eventref to merge with the present eventref.

`role`[¶](#gramps.gen.lib.eventref.EventRef.role)
Returns or sets role property

`serialize`()[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.serialize)[¶](#gramps.gen.lib.eventref.EventRef.serialize)
Convert the object to a serialized tuple of data.

`set_role`(*role*)[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.set_role)[¶](#gramps.gen.lib.eventref.EventRef.set_role)
Set the role according to the given argument.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/eventref.html#EventRef.unserialize)[¶](#gramps.gen.lib.eventref.EventRef.unserialize)
Convert a serialized tuple of data to an object.

### MediaRef[¶](#module-gramps.gen.lib.mediaref)
Media Reference class for Gramps.

*class *`gramps.gen.lib.mediaref.``MediaRef`(*source=None*)[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef)[¶](#gramps.gen.lib.mediaref.MediaRef)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase), [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.refbase.RefBase`](#gramps.gen.lib.refbase.RefBase), [`gramps.gen.lib.attrbase.AttributeBase`](#gramps.gen.lib.attrbase.AttributeBase)

Media reference class.

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.get_citation_child_list)[¶](#gramps.gen.lib.mediaref.MediaRef.get_citation_child_list)
Return the list of child secondary objects that may refer Citations.

Returns
Returns the list of child secondary child objects that may
refer Citations.

Return type
list

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.get_handle_referents)[¶](#gramps.gen.lib.mediaref.MediaRef.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects.

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.get_note_child_list)[¶](#gramps.gen.lib.mediaref.MediaRef.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_rectangle`()[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.get_rectangle)[¶](#gramps.gen.lib.mediaref.MediaRef.get_rectangle)
Return the subsection of an image.

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.get_referenced_handles)[¶](#gramps.gen.lib.mediaref.MediaRef.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.get_schema)[¶](#gramps.gen.lib.mediaref.MediaRef.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.get_text_data_child_list)[¶](#gramps.gen.lib.mediaref.MediaRef.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.is_equivalent)[¶](#gramps.gen.lib.mediaref.MediaRef.is_equivalent)
Return if this object reference is equivalent, that is agrees in
reference and region, to other.

Parameters
**other** ([*MediaRef*](#gramps.gen.lib.mediaref.MediaRef)) – The object reference to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.merge)[¶](#gramps.gen.lib.mediaref.MediaRef.merge)
Merge the content of acquisition into this object reference.

Lost: hlink and region or acquisition.

Parameters
**acquisition** ([*MediaRef*](#gramps.gen.lib.mediaref.MediaRef)) – The object reference to merge with the present one.

`serialize`()[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.serialize)[¶](#gramps.gen.lib.mediaref.MediaRef.serialize)
Convert the object to a serialized tuple of data.

`set_rectangle`(*coord*)[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.set_rectangle)[¶](#gramps.gen.lib.mediaref.MediaRef.set_rectangle)
Set subsection of an image.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/mediaref.html#MediaRef.unserialize)[¶](#gramps.gen.lib.mediaref.MediaRef.unserialize)
Convert a serialized tuple of data to an object.

### PersonRef[¶](#module-gramps.gen.lib.personref)
Person Reference class for Gramps.

*class *`gramps.gen.lib.personref.``PersonRef`(*source=None*)[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef)[¶](#gramps.gen.lib.personref.PersonRef)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase), [`gramps.gen.lib.citationbase.CitationBase`](#gramps.gen.lib.citationbase.CitationBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.refbase.RefBase`](#gramps.gen.lib.refbase.RefBase)

Person reference class.

This class is for keeping information about how the person relates
to another person from the database, if not through family.
Examples would be: godparent, friend, etc.

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.get_handle_referents)[¶](#gramps.gen.lib.personref.PersonRef.get_handle_referents)
Return the list of child objects which may, directly or through
their children, reference primary objects..

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.get_note_child_list)[¶](#gramps.gen.lib.personref.PersonRef.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.get_referenced_handles)[¶](#gramps.gen.lib.personref.PersonRef.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

`get_relation`()[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.get_relation)[¶](#gramps.gen.lib.personref.PersonRef.get_relation)
Return the relation to a person.

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.get_schema)[¶](#gramps.gen.lib.personref.PersonRef.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.get_text_data_child_list)[¶](#gramps.gen.lib.personref.PersonRef.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.get_text_data_list)[¶](#gramps.gen.lib.personref.PersonRef.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.is_equivalent)[¶](#gramps.gen.lib.personref.PersonRef.is_equivalent)
Return if this person reference is equivalent, that is agrees in handle
and relation, to other.

Parameters
**other** ([*PersonRef*](#gramps.gen.lib.personref.PersonRef)) – The personref to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.merge)[¶](#gramps.gen.lib.personref.PersonRef.merge)
Merge the content of acquisition into this person reference.

Lost: hlink and relation of acquisition.

Parameters
**acquisition** ([*PersonRef*](#gramps.gen.lib.personref.PersonRef)) – The personref to merge with the present personref.

`serialize`()[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.serialize)[¶](#gramps.gen.lib.personref.PersonRef.serialize)
Convert the object to a serialized tuple of data.

`set_relation`(*rel*)[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.set_relation)[¶](#gramps.gen.lib.personref.PersonRef.set_relation)
Set relation to a person.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/personref.html#PersonRef.unserialize)[¶](#gramps.gen.lib.personref.PersonRef.unserialize)
Convert a serialized tuple of data to an object.

### PlaceRef[¶](#module-gramps.gen.lib.placeref)
Place Reference class for Gramps

*class *`gramps.gen.lib.placeref.``PlaceRef`(*source=None*)[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef)[¶](#gramps.gen.lib.placeref.PlaceRef)
Bases: [`gramps.gen.lib.refbase.RefBase`](#gramps.gen.lib.refbase.RefBase), [`gramps.gen.lib.datebase.DateBase`](#gramps.gen.lib.datebase.DateBase), [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject)

Place reference class.

This class is for keeping information about how places link to other places
in the place hierarchy.

`get_citation_child_list`()[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.get_citation_child_list)[¶](#gramps.gen.lib.placeref.PlaceRef.get_citation_child_list)
Return the list of child secondary objects that may refer citations.

Returns
Returns the list of child secondary child objects that may
refer citations.

Return type
list

`get_handle_referents`()[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.get_handle_referents)[¶](#gramps.gen.lib.placeref.PlaceRef.get_handle_referents)
Return the list of child objects which may, directly or through their
children, reference primary objects..

Returns
Returns the list of objects referencing primary objects.

Return type
list

`get_note_child_list`()[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.get_note_child_list)[¶](#gramps.gen.lib.placeref.PlaceRef.get_note_child_list)
Return the list of child secondary objects that may refer notes.

Returns
Returns the list of child secondary child objects that may
refer notes.

Return type
list

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.get_referenced_handles)[¶](#gramps.gen.lib.placeref.PlaceRef.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
Returns the list of (classname, handle) tuples for referenced
objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.get_schema)[¶](#gramps.gen.lib.placeref.PlaceRef.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_child_list`()[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.get_text_data_child_list)[¶](#gramps.gen.lib.placeref.PlaceRef.get_text_data_child_list)
Return the list of child objects that may carry textual data.

Returns
Returns the list of child objects that may carry textual data.

Return type
list

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.get_text_data_list)[¶](#gramps.gen.lib.placeref.PlaceRef.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.is_equivalent)[¶](#gramps.gen.lib.placeref.PlaceRef.is_equivalent)
Return if this eventref is equivalent, that is agrees in handle and
role, to other.

Parameters
**other** ([*PlaceRef*](#gramps.gen.lib.placeref.PlaceRef)) – The eventref to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`serialize`()[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.serialize)[¶](#gramps.gen.lib.placeref.PlaceRef.serialize)
Convert the object to a serialized tuple of data.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/placeref.html#PlaceRef.unserialize)[¶](#gramps.gen.lib.placeref.PlaceRef.unserialize)
Convert a serialized tuple of data to an object.

### RepoRef[¶](#module-gramps.gen.lib.reporef)
Repository Reference class for Gramps

*class *`gramps.gen.lib.reporef.``RepoRef`(*source=None*)[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef)[¶](#gramps.gen.lib.reporef.RepoRef)
Bases: [`gramps.gen.lib.secondaryobj.SecondaryObject`](#gramps.gen.lib.secondaryobj.SecondaryObject), [`gramps.gen.lib.privacybase.PrivacyBase`](#gramps.gen.lib.privacybase.PrivacyBase), [`gramps.gen.lib.notebase.NoteBase`](#gramps.gen.lib.notebase.NoteBase), [`gramps.gen.lib.refbase.RefBase`](#gramps.gen.lib.refbase.RefBase)

Repository reference class.

`get_call_number`()[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.get_call_number)[¶](#gramps.gen.lib.reporef.RepoRef.get_call_number)

`get_media_type`()[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.get_media_type)[¶](#gramps.gen.lib.reporef.RepoRef.get_media_type)

`get_referenced_handles`()[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.get_referenced_handles)[¶](#gramps.gen.lib.reporef.RepoRef.get_referenced_handles)
Return the list of (classname, handle) tuples for all directly
referenced primary objects.

Returns
List of (classname, handle) tuples for referenced objects.

Return type
list

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.get_schema)[¶](#gramps.gen.lib.reporef.RepoRef.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.get_text_data_list)[¶](#gramps.gen.lib.reporef.RepoRef.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`is_equivalent`(*other*)[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.is_equivalent)[¶](#gramps.gen.lib.reporef.RepoRef.is_equivalent)
Return if this repository reference is equivalent, that is agrees in
reference, call number and medium, to other.

Parameters
**other** ([*RepoRef*](#gramps.gen.lib.reporef.RepoRef)) – The repository reference to compare this one to.

Returns
Constant indicating degree of equivalence.

Return type
int

`merge`(*acquisition*)[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.merge)[¶](#gramps.gen.lib.reporef.RepoRef.merge)
Merge the content of acquisition into this repository reference.

Parameters
**acquisition** ([*RepoRef*](#gramps.gen.lib.reporef.RepoRef)) – The repository reference to merge with the present
repository reference.

`serialize`()[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.serialize)[¶](#gramps.gen.lib.reporef.RepoRef.serialize)
Convert the object to a serialized tuple of data.

`set_call_number`(*number*)[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.set_call_number)[¶](#gramps.gen.lib.reporef.RepoRef.set_call_number)

`set_media_type`(*media_type*)[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.set_media_type)[¶](#gramps.gen.lib.reporef.RepoRef.set_media_type)

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/reporef.html#RepoRef.unserialize)[¶](#gramps.gen.lib.reporef.RepoRef.unserialize)
Convert a serialized tuple of data to an object.

## Table objects[¶](#table-objects)

### Table object[¶](#module-gramps.gen.lib.tableobj)
Table Object class for Gramps.

*class *`gramps.gen.lib.tableobj.``TableObject`(*source=None*)[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject)[¶](#gramps.gen.lib.tableobj.TableObject)
Bases: [`gramps.gen.lib.baseobj.BaseObject`](#gramps.gen.lib.baseobj.BaseObject)

The TableObject is the base class for all objects that are stored in a
seperate database table. Each object has a database handle and a last
changed time. The database handle is used as the unique key for a record
in the database. This is not the same as the Gramps ID, which is a user
visible identifier for a record.

It is the base class for the BasicPrimaryObject class and Tag class.

`get_change_display`()[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject.get_change_display)[¶](#gramps.gen.lib.tableobj.TableObject.get_change_display)
Return the string representation of the last change time.

Returns
string representation of the last change time.

Return type
str

`get_change_time`()[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject.get_change_time)[¶](#gramps.gen.lib.tableobj.TableObject.get_change_time)
Return the time that the data was last changed.

The value in the format returned by the `time.time()` command.

Returns
Time that the data was last changed. The value in the format
returned by the `time.time()` command.

Return type
int

`get_handle`()[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject.get_handle)[¶](#gramps.gen.lib.tableobj.TableObject.get_handle)
Return the database handle for the primary object.

Returns
database handle associated with the object

Return type
str

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject.get_schema)[¶](#gramps.gen.lib.tableobj.TableObject.get_schema)
Return schema.

*classmethod *`get_secondary_fields`()[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject.get_secondary_fields)[¶](#gramps.gen.lib.tableobj.TableObject.get_secondary_fields)
Return all secondary fields and their types

`serialize`()[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject.serialize)[¶](#gramps.gen.lib.tableobj.TableObject.serialize)
Convert the object to a serialized tuple of data.

`set_change_time`(*change*)[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject.set_change_time)[¶](#gramps.gen.lib.tableobj.TableObject.set_change_time)
Modify the time that the data was last changed.

The value must be in the format returned by the `time.time()`
command.

Parameters
**change** (int in format as `time.time()` command) – new time

`set_handle`(*handle*)[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject.set_handle)[¶](#gramps.gen.lib.tableobj.TableObject.set_handle)
Set the database handle for the primary object.

Parameters
**handle** (*str*) – object database handle

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/tableobj.html#TableObject.unserialize)[¶](#gramps.gen.lib.tableobj.TableObject.unserialize)
Convert a serialized tuple of data to an object.

### Tag[¶](#module-gramps.gen.lib.tag)
Tag object for Gramps.

*class *`gramps.gen.lib.tag.``Tag`(*source=None*)[[source]](../_modules/gramps/gen/lib/tag.html#Tag)[¶](#gramps.gen.lib.tag.Tag)
Bases: [`gramps.gen.lib.tableobj.TableObject`](#gramps.gen.lib.tableobj.TableObject)

The Tag record is used to store information about a tag that can be
attached to a primary object.

`are_equal`(*other*)[[source]](../_modules/gramps/gen/lib/tag.html#Tag.are_equal)[¶](#gramps.gen.lib.tag.Tag.are_equal)
Return True if the passed Tag is equivalent to the current Tag.

Parameters
**other** ([*Tag*](#gramps.gen.lib.tag.Tag)) – Tag to compare against

Returns
True if the Tags are equal

Return type
bool

`color`[¶](#gramps.gen.lib.tag.Tag.color)
Returns or sets color of the tag

`get_color`()[[source]](../_modules/gramps/gen/lib/tag.html#Tag.get_color)[¶](#gramps.gen.lib.tag.Tag.get_color)
Return the color of the Tag.

Returns
Returns the color of the Tag

Return type
str

`get_name`()[[source]](../_modules/gramps/gen/lib/tag.html#Tag.get_name)[¶](#gramps.gen.lib.tag.Tag.get_name)
Return the name of the Tag.

Returns
Name of the Tag

Return type
str

`get_priority`()[[source]](../_modules/gramps/gen/lib/tag.html#Tag.get_priority)[¶](#gramps.gen.lib.tag.Tag.get_priority)
Return the priority of the Tag.

Returns
Returns the priority of the Tag

Return type
int

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/tag.html#Tag.get_schema)[¶](#gramps.gen.lib.tag.Tag.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_text_data_list`()[[source]](../_modules/gramps/gen/lib/tag.html#Tag.get_text_data_list)[¶](#gramps.gen.lib.tag.Tag.get_text_data_list)
Return the list of all textual attributes of the object.

Returns
Returns the list of all textual attributes of the object.

Return type
list

`is_empty`()[[source]](../_modules/gramps/gen/lib/tag.html#Tag.is_empty)[¶](#gramps.gen.lib.tag.Tag.is_empty)
Return True if the Tag is an empty object (no values set).

Returns
True if the Tag is empty

Return type
bool

`name`[¶](#gramps.gen.lib.tag.Tag.name)
Returns or sets name of the tag

`priority`[¶](#gramps.gen.lib.tag.Tag.priority)
Returns or sets priority of the tag

`serialize`()[[source]](../_modules/gramps/gen/lib/tag.html#Tag.serialize)[¶](#gramps.gen.lib.tag.Tag.serialize)
Convert the data held in the event to a Python tuple that
represents all the data elements.

This method is used to convert the object into a form that can easily
be saved to a database.

These elements may be primitive Python types (string, integers),
complex Python types (lists or tuples, or Python objects. If the
target database cannot handle complex types (such as objects or
lists), the database is responsible for converting the data into
a form that it can use.

Returns
Returns a python tuple containing the data that should
be considered persistent.

Return type
tuple

`set_color`(*color*)[[source]](../_modules/gramps/gen/lib/tag.html#Tag.set_color)[¶](#gramps.gen.lib.tag.Tag.set_color)
Set the color of the Tag to the passed string.

The string is of the format #rrrrggggbbbb.

Parameters
**color** (*str*) – Color to assign to the Tag

`set_name`(*name*)[[source]](../_modules/gramps/gen/lib/tag.html#Tag.set_name)[¶](#gramps.gen.lib.tag.Tag.set_name)
Set the name of the Tag to the passed string.

Parameters
**name** (*str*) – Name to assign to the Tag

`set_priority`(*priority*)[[source]](../_modules/gramps/gen/lib/tag.html#Tag.set_priority)[¶](#gramps.gen.lib.tag.Tag.set_priority)
Set the priority of the Tag to the passed integer.

The lower the value the higher the priority.

Parameters
**priority** (*int*) – Priority to assign to the Tag

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/tag.html#Tag.unserialize)[¶](#gramps.gen.lib.tag.Tag.unserialize)
Convert the data held in a tuple created by the serialize method
back into the data in a Tag structure.

Parameters
**data** (*tuple*) – tuple containing the persistent data associated with the
object

## Date objects[¶](#module-gramps.gen.lib.date)
Support for dates.

### Date[¶](#date)

*class *`gramps.gen.lib.date.``Date`(**source*)[[source]](../_modules/gramps/gen/lib/date.html#Date)[¶](#gramps.gen.lib.date.Date)
Bases: `object`

The core date handling class for Gramps.

Supports partial dates, compound dates and alternate calendars.

`CALENDARS`* = range(0, 7)*[¶](#gramps.gen.lib.date.Date.CALENDARS)

`CAL_FRENCH`* = 3*[¶](#gramps.gen.lib.date.Date.CAL_FRENCH)

`CAL_GREGORIAN`* = 0*[¶](#gramps.gen.lib.date.Date.CAL_GREGORIAN)

`CAL_HEBREW`* = 2*[¶](#gramps.gen.lib.date.Date.CAL_HEBREW)

`CAL_ISLAMIC`* = 5*[¶](#gramps.gen.lib.date.Date.CAL_ISLAMIC)

`CAL_JULIAN`* = 1*[¶](#gramps.gen.lib.date.Date.CAL_JULIAN)

`CAL_PERSIAN`* = 4*[¶](#gramps.gen.lib.date.Date.CAL_PERSIAN)

`CAL_SWEDISH`* = 6*[¶](#gramps.gen.lib.date.Date.CAL_SWEDISH)

`EMPTY`* = (0, 0, 0, False)*[¶](#gramps.gen.lib.date.Date.EMPTY)

`MOD_ABOUT`* = 3*[¶](#gramps.gen.lib.date.Date.MOD_ABOUT)

`MOD_AFTER`* = 2*[¶](#gramps.gen.lib.date.Date.MOD_AFTER)

`MOD_BEFORE`* = 1*[¶](#gramps.gen.lib.date.Date.MOD_BEFORE)

`MOD_NONE`* = 0*[¶](#gramps.gen.lib.date.Date.MOD_NONE)

`MOD_RANGE`* = 4*[¶](#gramps.gen.lib.date.Date.MOD_RANGE)

`MOD_SPAN`* = 5*[¶](#gramps.gen.lib.date.Date.MOD_SPAN)

`MOD_TEXTONLY`* = 6*[¶](#gramps.gen.lib.date.Date.MOD_TEXTONLY)

`NEWYEAR_JAN1`* = 0*[¶](#gramps.gen.lib.date.Date.NEWYEAR_JAN1)

`NEWYEAR_MAR1`* = 1*[¶](#gramps.gen.lib.date.Date.NEWYEAR_MAR1)

`NEWYEAR_MAR25`* = 2*[¶](#gramps.gen.lib.date.Date.NEWYEAR_MAR25)

`NEWYEAR_SEP1`* = 3*[¶](#gramps.gen.lib.date.Date.NEWYEAR_SEP1)

`QUAL_CALCULATED`* = 2*[¶](#gramps.gen.lib.date.Date.QUAL_CALCULATED)

`QUAL_ESTIMATED`* = 1*[¶](#gramps.gen.lib.date.Date.QUAL_ESTIMATED)

`QUAL_NONE`* = 0*[¶](#gramps.gen.lib.date.Date.QUAL_NONE)

`calendar_names`* = ['Gregorian', 'Julian', 'Hebrew', 'French Republican', 'Persian', 'Islamic', 'Swedish']*[¶](#gramps.gen.lib.date.Date.calendar_names)

`convert_calendar`(*calendar*, *known_valid=True*)[[source]](../_modules/gramps/gen/lib/date.html#Date.convert_calendar)[¶](#gramps.gen.lib.date.Date.convert_calendar)
Convert the date from the current calendar to the specified calendar.

`copy`(*source*)[[source]](../_modules/gramps/gen/lib/date.html#Date.copy)[¶](#gramps.gen.lib.date.Date.copy)
Copy all the attributes of the given Date instance to the present
instance, without creating a new object.

`copy_offset_ymd`(*year=0*, *month=0*, *day=0*)[[source]](../_modules/gramps/gen/lib/date.html#Date.copy_offset_ymd)[¶](#gramps.gen.lib.date.Date.copy_offset_ymd)
Return a Date copy based on year, month, and day offset.

`copy_ymd`(*year=0*, *month=0*, *day=0*, *remove_stop_date=None*)[[source]](../_modules/gramps/gen/lib/date.html#Date.copy_ymd)[¶](#gramps.gen.lib.date.Date.copy_ymd)
Return a Date copy with year, month, and day set.

Parameters
**remove_stop_date** – Same as in set_yr_mon_day.

`get_calendar`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_calendar)[¶](#gramps.gen.lib.date.Date.get_calendar)
Return an integer indicating the calendar selected.

The valid values are:

| Table |
|-------|

| CAL_GREGORIAN

 |
Gregorian calendar

 |
 |
| CAL_JULIAN

 |
Julian calendar

 |
 |
| CAL_HEBREW

 |
Hebrew (Jewish) calendar

 |
 |
| CAL_FRENCH

 |
French Republican calendar

 |
 |
| CAL_PERSIAN

 |
Persian calendar

 |
 |
| CAL_ISLAMIC

 |
Islamic calendar

 |
 |
| CAL_SWEDISH

 |
Swedish calendar 1700-03-01 -> 1712-02-30!

 |
 |

`get_day`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_day)[¶](#gramps.gen.lib.date.Date.get_day)
Return the day of the month associated with the date.

If the day is not defined, a zero is returned. If the date is a
compound date, the lower date day is returned.

`get_day_valid`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_day_valid)[¶](#gramps.gen.lib.date.Date.get_day_valid)
Return true if the day is valid.

`get_dmy`(*get_slash=False*)[[source]](../_modules/gramps/gen/lib/date.html#Date.get_dmy)[¶](#gramps.gen.lib.date.Date.get_dmy)
Return (day, month, year, [slash]).

`get_dow`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_dow)[¶](#gramps.gen.lib.date.Date.get_dow)
Return an integer representing the day of the week associated with the
date (Monday=0).

If the day is not defined, a None is returned. If the date is a
compound date, the lower date day is returned.

`get_high_year`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_high_year)[¶](#gramps.gen.lib.date.Date.get_high_year)
Return the high year estimate.

For compound dates with non-zero stop year, the stop year is returned.
Otherwise, the start year is returned.

`get_modifier`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_modifier)[¶](#gramps.gen.lib.date.Date.get_modifier)
Return an integer indicating the calendar selected.

The valid values are:

| Table |
|-------|

| MOD_NONE

 |
no modifier (default)

 |
 |
| MOD_BEFORE

 |
before

 |
 |
| MOD_AFTER

 |
after

 |
 |
| MOD_ABOUT

 |
about

 |
 |
| MOD_RANGE

 |
date range

 |
 |
| MOD_SPAN

 |
date span

 |
 |
| MOD_TEXTONLY

 |
text only

 |
 |

`get_month`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_month)[¶](#gramps.gen.lib.date.Date.get_month)
Return the month associated with the date.

If the month is not defined, a zero is returned. If the date is a
compound date, the lower date month is returned.

`get_month_valid`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_month_valid)[¶](#gramps.gen.lib.date.Date.get_month_valid)
Return true if the month is valid

`get_new_year`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_new_year)[¶](#gramps.gen.lib.date.Date.get_new_year)
Return the new year code associated with the date.

`get_quality`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_quality)[¶](#gramps.gen.lib.date.Date.get_quality)
Return an integer indicating the calendar selected.

The valid values are:

| Table |
|-------|

| QUAL_NONE

 |
normal (default)

 |
 |
| QUAL_ESTIMATED

 |
estimated

 |
 |
| QUAL_CALCULATED

 |
calculated

 |
 |

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_schema)[¶](#gramps.gen.lib.date.Date.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_slash`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_slash)[¶](#gramps.gen.lib.date.Date.get_slash)
Return true if the date is a slash-date (dual dated).

`get_slash2`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_slash2)[¶](#gramps.gen.lib.date.Date.get_slash2)
Return true if the ending date is a slash-date (dual dated).

`get_sort_value`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_sort_value)[¶](#gramps.gen.lib.date.Date.get_sort_value)
Return the sort value of Date object.

If the value is a text string, 0 is returned. Otherwise, the
calculated sort date is returned. The sort date is rebuilt on every
assignment.

The sort value is an integer representing the value. The sortval is
the integer number of days that have elapsed since Monday, January 1,
4713 BC in the proleptic Julian calendar.

See also

[http://en.wikipedia.org/wiki/Julian_day](http://en.wikipedia.org/wiki/Julian_day)

`get_start_date`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_start_date)[¶](#gramps.gen.lib.date.Date.get_start_date)
Return a tuple representing the start date.

If the date is a compound date (range or a span), it is the first part
of the compound date. If the date is a text string, a tuple of
(0, 0, 0, False) is returned. Otherwise, a date of (DD, MM, YY, slash)
is returned. If slash is True, then the date is in the form of 1530/1.

`get_start_stop_range`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_start_stop_range)[¶](#gramps.gen.lib.date.Date.get_start_stop_range)
Return the minimal start_date, and a maximal stop_date corresponding
to this date, given in Gregorian calendar.

Useful in doing range overlap comparisons between different dates.

Note that we stay in (YR,MON,DAY)

`get_stop_date`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_stop_date)[¶](#gramps.gen.lib.date.Date.get_stop_date)
Return a tuple representing the second half of a compound date.

If the date is not a compound date, (including text strings) a tuple
of (0, 0, 0, False) is returned. Otherwise, a date of (DD, MM, YY, slash)
is returned. If slash is True, then the date is in the form of 1530/1.

`get_stop_day`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_stop_day)[¶](#gramps.gen.lib.date.Date.get_stop_day)
Return the day of the month associated with the second part of a
compound date.

If the day is not defined, a zero is returned.

`get_stop_month`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_stop_month)[¶](#gramps.gen.lib.date.Date.get_stop_month)
Return the month of the month associated with the second part of a
compound date.

If the month is not defined, a zero is returned.

`get_stop_year`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_stop_year)[¶](#gramps.gen.lib.date.Date.get_stop_year)
Return the day of the year associated with the second part of a
compound date.

If the year is not defined, a zero is returned.

`get_stop_ymd`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_stop_ymd)[¶](#gramps.gen.lib.date.Date.get_stop_ymd)
Return (year, month, day) of the stop date, or all-zeros if it’s not
defined.

`get_text`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_text)[¶](#gramps.gen.lib.date.Date.get_text)
Return the text value associated with an invalid date.

`get_valid`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_valid)[¶](#gramps.gen.lib.date.Date.get_valid)
Return true if any part of the date is valid.

`get_year`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_year)[¶](#gramps.gen.lib.date.Date.get_year)
Return the year associated with the date.

If the year is not defined, a zero is returned. If the date is a
compound date, the lower date year is returned.

`get_year_calendar`(*calendar_name=None*)[[source]](../_modules/gramps/gen/lib/date.html#Date.get_year_calendar)[¶](#gramps.gen.lib.date.Date.get_year_calendar)
Return the year of this date in the calendar name given.

Defaults to self’s calendar if one is not given.

```
>>> Date(2009, 12, 8).to_calendar("hebrew").get_year_calendar()
5770

```

`get_year_valid`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_year_valid)[¶](#gramps.gen.lib.date.Date.get_year_valid)
Return true if the year is valid.

`get_ymd`()[[source]](../_modules/gramps/gen/lib/date.html#Date.get_ymd)[¶](#gramps.gen.lib.date.Date.get_ymd)
Return (year, month, day).

`is_compound`()[[source]](../_modules/gramps/gen/lib/date.html#Date.is_compound)[¶](#gramps.gen.lib.date.Date.is_compound)
Return True if the date is a date range or a date span.

`is_empty`()[[source]](../_modules/gramps/gen/lib/date.html#Date.is_empty)[¶](#gramps.gen.lib.date.Date.is_empty)
Return True if the date contains no information (empty text).

`is_equal`(*other*)[[source]](../_modules/gramps/gen/lib/date.html#Date.is_equal)[¶](#gramps.gen.lib.date.Date.is_equal)
Return 1 if the given Date instance is the same as the present
instance IN ALL REGARDS.

Needed, because the __cmp__ only looks at the sorting value, and
ignores the modifiers/comments.

`is_full`()[[source]](../_modules/gramps/gen/lib/date.html#Date.is_full)[¶](#gramps.gen.lib.date.Date.is_full)
Return True if the date is fully specified.

`is_regular`()[[source]](../_modules/gramps/gen/lib/date.html#Date.is_regular)[¶](#gramps.gen.lib.date.Date.is_regular)
Return True if the date is a regular date.

The regular date is a single exact date, i.e. not text-only, not
a range or a span, not estimated/calculated, not about/before/after
date, and having year, month, and day all non-zero.

`is_valid`()[[source]](../_modules/gramps/gen/lib/date.html#Date.is_valid)[¶](#gramps.gen.lib.date.Date.is_valid)
Return true if any part of the date is valid.

`lookup_calendar`(*calendar*)[[source]](../_modules/gramps/gen/lib/date.html#Date.lookup_calendar)[¶](#gramps.gen.lib.date.Date.lookup_calendar)
Lookup calendar name in the list of known calendars, even if translated.

`lookup_modifier`(*modifier*)[[source]](../_modules/gramps/gen/lib/date.html#Date.lookup_modifier)[¶](#gramps.gen.lib.date.Date.lookup_modifier)
Lookup date modifier keyword, even if translated.

`lookup_quality`(*quality*)[[source]](../_modules/gramps/gen/lib/date.html#Date.lookup_quality)[¶](#gramps.gen.lib.date.Date.lookup_quality)
Lookup date quality keyword, even if translated.

`make_vague`()[[source]](../_modules/gramps/gen/lib/date.html#Date.make_vague)[¶](#gramps.gen.lib.date.Date.make_vague)
Remove month and day details to make the date approximate.

`match`(*other_date*, *comparison='='*)[[source]](../_modules/gramps/gen/lib/date.html#Date.match)[¶](#gramps.gen.lib.date.Date.match)
Compare two dates using sophisticated techniques looking for any match
between two possible dates, date spans and qualities.

The other comparisons for Date (is_equal() and __cmp() don’t actually
look for anything other than a straight match, or a simple comparison
of the sortval.

| Table |
|-------|

| Comparison

 |
Returns

 |
 |

| =,==

 |
True if any part of other_date matches any part of self

 |
 |
|

 |
True if any part of other_date > any part of self

 |
 |
| >>

 |
True if all parts of other_date > all parts of self

 |
 |

`match_exact`(*other_date*)[[source]](../_modules/gramps/gen/lib/date.html#Date.match_exact)[¶](#gramps.gen.lib.date.Date.match_exact)
Perform an extact match between two dates. The dates are not treated
as being person-centric. This is used to match date ranges in places.

*static *`newyear_to_code`(*string*)[[source]](../_modules/gramps/gen/lib/date.html#Date.newyear_to_code)[¶](#gramps.gen.lib.date.Date.newyear_to_code)

Return newyear code of string, where string is:‘’, ‘Jan1’, ‘Mar1’, ‘3-25’, ‘9-1’, etc.

`newyear_to_str`()[[source]](../_modules/gramps/gen/lib/date.html#Date.newyear_to_str)[¶](#gramps.gen.lib.date.Date.newyear_to_str)
Return the string representation of the newyear.

`offset`(*value*)[[source]](../_modules/gramps/gen/lib/date.html#Date.offset)[¶](#gramps.gen.lib.date.Date.offset)
Return (year, month, day) of this date +- value.

`offset_date`(*value*)[[source]](../_modules/gramps/gen/lib/date.html#Date.offset_date)[¶](#gramps.gen.lib.date.Date.offset_date)
Return (year, month, day) of this date +- value.

`recalc_sort_value`()[[source]](../_modules/gramps/gen/lib/date.html#Date.recalc_sort_value)[¶](#gramps.gen.lib.date.Date.recalc_sort_value)
Recalculates the numerical sort value associated with the date
and returns it. Public method.

`serialize`(*no_text_date=False*)[[source]](../_modules/gramps/gen/lib/date.html#Date.serialize)[¶](#gramps.gen.lib.date.Date.serialize)
Convert to a series of tuples for data storage.

`set`(*quality=None*, *modifier=None*, *calendar=None*, *value=None*, *text=None*, *newyear=0*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set)[¶](#gramps.gen.lib.date.Date.set)
Set the date to the specified value.

Parameters

- **quality** – The date quality for the date (see [`get_quality()`](#gramps.gen.lib.date.Date.get_quality)
for more information).
Defaults to the previous value for the date.

- **modified** – The date modifier for the date (see
[`get_modifier()`](#gramps.gen.lib.date.Date.get_modifier) for more information)
Defaults to the previous value for the date.

- **calendar** – The calendar associated with the date (see
[`get_calendar()`](#gramps.gen.lib.date.Date.get_calendar) for more information).
Defaults to the previous value for the date.

- **value** – A tuple representing the date information. For a
non-compound date, the format is (DD, MM, YY, slash)
and for a compound date the tuple stores data as
(DD, MM, YY, slash1, DD, MM, YY, slash2)
Defaults to the previous value for the date.

- **text** – A text string holding either the verbatim user input
or a comment relating to the date.
Defaults to the previous value for the date.

- **newyear** – The newyear code, or tuple representing (month, day)
of newyear day.
Defaults to 0.

The sort value is recalculated.

`set2_yr_mon_day`(*year*, *month*, *day*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set2_yr_mon_day)[¶](#gramps.gen.lib.date.Date.set2_yr_mon_day)
Set the year, month, and day values in the 2nd part of
a compound date (range or span).

`set2_yr_mon_day_offset`(*year=0*, *month=0*, *day=0*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set2_yr_mon_day_offset)[¶](#gramps.gen.lib.date.Date.set2_yr_mon_day_offset)
Set the year, month, and day values by offset in the 2nd part
of a compound date (range or span).

`set_as_text`(*text*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_as_text)[¶](#gramps.gen.lib.date.Date.set_as_text)
Set the day to a text string, and assign the sort value to zero.

`set_calendar`(*val*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_calendar)[¶](#gramps.gen.lib.date.Date.set_calendar)
Set the calendar selected for the date.

`set_modifier`(*val*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_modifier)[¶](#gramps.gen.lib.date.Date.set_modifier)
Set the modifier for the date.

`set_new_year`(*value*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_new_year)[¶](#gramps.gen.lib.date.Date.set_new_year)
Set the new year code associated with the date.

`set_quality`(*val*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_quality)[¶](#gramps.gen.lib.date.Date.set_quality)
Set the quality selected for the date.

`set_slash`(*value*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_slash)[¶](#gramps.gen.lib.date.Date.set_slash)
Set to 1 if the date is a slash-date (dual dated).

`set_slash2`(*value*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_slash2)[¶](#gramps.gen.lib.date.Date.set_slash2)
Set to 1 if the ending date is a slash-date (dual dated).

`set_text_value`(*text*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_text_value)[¶](#gramps.gen.lib.date.Date.set_text_value)
Set the text string to a given text.

`set_year`(*year*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_year)[¶](#gramps.gen.lib.date.Date.set_year)
Set the year value.

`set_yr_mon_day`(*year*, *month*, *day*, *remove_stop_date=None*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_yr_mon_day)[¶](#gramps.gen.lib.date.Date.set_yr_mon_day)
Set the year, month, and day values.

Parameters
**remove_stop_date** – Required parameter for a compound date.
When True, the stop date is changed to the same date as well.
When False, the stop date is not changed.

`set_yr_mon_day_offset`(*year=0*, *month=0*, *day=0*)[[source]](../_modules/gramps/gen/lib/date.html#Date.set_yr_mon_day_offset)[¶](#gramps.gen.lib.date.Date.set_yr_mon_day_offset)
Offset the date by the given year, month, and day values.

`to_calendar`(*calendar_name*)[[source]](../_modules/gramps/gen/lib/date.html#Date.to_calendar)[¶](#gramps.gen.lib.date.Date.to_calendar)
Return a new Date object in the calendar calendar_name.

```
>>> Date(1591, 1, 1).to_calendar("julian")
1590-12-22 (Julian)

```

`ui_calendar_names`* = ['Gregorian', 'Julian', 'Hebrew', 'French Republican', 'Persian', 'Islamic', 'Swedish']*[¶](#gramps.gen.lib.date.Date.ui_calendar_names)

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/date.html#Date.unserialize)[¶](#gramps.gen.lib.date.Date.unserialize)
Load from the format created by serialize.

`year`[¶](#gramps.gen.lib.date.Date.year)
Return the year associated with the date.

If the year is not defined, a zero is returned. If the date is a
compound date, the lower date year is returned.

### Span[¶](#span)

*class *`gramps.gen.lib.date.``Span`(*date1*, *date2*)[[source]](../_modules/gramps/gen/lib/date.html#Span)[¶](#gramps.gen.lib.date.Span)
Bases: `object`

Span is used to represent the difference between two dates for three
main purposes: sorting, ranking, and describing.

sort = (base day count, offset)
minmax = (min days, max days)

`ABOUT`* = 50*[¶](#gramps.gen.lib.date.Span.ABOUT)

`AFTER`* = 50*[¶](#gramps.gen.lib.date.Span.AFTER)

`ALIVE`* = 110*[¶](#gramps.gen.lib.date.Span.ALIVE)

`BEFORE`* = 50*[¶](#gramps.gen.lib.date.Span.BEFORE)

`as_age`()[[source]](../_modules/gramps/gen/lib/date.html#Span.as_age)[¶](#gramps.gen.lib.date.Span.as_age)
Get Span as an age (will not return more than Span.ALIVE).

`as_time`()[[source]](../_modules/gramps/gen/lib/date.html#Span.as_time)[¶](#gramps.gen.lib.date.Span.as_time)
Get Span as a time (can be greater than Span.ALIVE).

`format`(*precision=2*, *as_age=True*, *dlocale=*)[[source]](../_modules/gramps/gen/lib/date.html#Span.format)[¶](#gramps.gen.lib.date.Span.format)
Force a string representation at a level of precision.

| Table |
|-------|

| 1

 |
only most significant level (year, month, day)

 |
 |
| 2

 |
only most two significant levels (year, month, day)

 |
 |
| 3

 |
at most three items of signifance (year, month, day)

 |
 |

If dlocale is passed in (a [`GrampsLocale`](gen_utils.html#gramps.gen.utils.grampslocale.GrampsLocale)) then
the translated value will be returned instead.

Parameters
**dlocale** (a [`GrampsLocale`](gen_utils.html#gramps.gen.utils.grampslocale.GrampsLocale) instance) – allow deferred translation of strings

`get_repr`(*as_age=False*, *dlocale=*)[[source]](../_modules/gramps/gen/lib/date.html#Span.get_repr)[¶](#gramps.gen.lib.date.Span.get_repr)
Get the representation as a time or age.

If dlocale is passed in (a [`GrampsLocale`](gen_utils.html#gramps.gen.utils.grampslocale.GrampsLocale)) then
the translated value will be returned instead.

Parameters
**dlocale** (a [`GrampsLocale`](gen_utils.html#gramps.gen.utils.grampslocale.GrampsLocale) instance) – allow deferred translation of strings

`is_valid`()[[source]](../_modules/gramps/gen/lib/date.html#Span.is_valid)[¶](#gramps.gen.lib.date.Span.is_valid)

`tuple`()[[source]](../_modules/gramps/gen/lib/date.html#Span.tuple)[¶](#gramps.gen.lib.date.Span.tuple)

### DateError[¶](#dateerror)

*exception *`gramps.gen.lib.date.``DateError`(*value=''*)[[source]](../_modules/gramps/gen/errors.html#DateError)[¶](#gramps.gen.lib.date.DateError)
Error used to report Date errors

Might have a .date attribute holding an invalid Date object
that triggered the error.

## Text objects[¶](#text-objects)

### StyledTextTag[¶](#module-gramps.gen.lib.styledtexttag)
Provide formatting tag definition for StyledText.

*class *`gramps.gen.lib.styledtexttag.``StyledTextTag`(*name=None*, *value=None*, *ranges=None*)[[source]](../_modules/gramps/gen/lib/styledtexttag.html#StyledTextTag)[¶](#gramps.gen.lib.styledtexttag.StyledTextTag)
Bases: `object`

Hold formatting information for [`StyledText`](#gramps.gen.lib.styledtext.StyledText).

[`StyledTextTag`](#gramps.gen.lib.styledtexttag.StyledTextTag) is a container class, it’s attributes are
directly accessed.

Variables

- [**name**](../simple.html#gramps.gen.simple._simpleaccess.SimpleAccess.name) – Type (or name) of the tag instance. E.g. ‘bold’, etc.

- [**value**](#gramps.gen.lib.grampstype.GrampsType.value) – Value of the tag. E.g. color hex string for font color, etc.

- **ranges** – Pointer pairs into the string, where the tag applies.

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/styledtexttag.html#StyledTextTag.get_schema)[¶](#gramps.gen.lib.styledtexttag.StyledTextTag.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`serialize`()[[source]](../_modules/gramps/gen/lib/styledtexttag.html#StyledTextTag.serialize)[¶](#gramps.gen.lib.styledtexttag.StyledTextTag.serialize)
Convert the object to a serialized tuple of data.

Returns
Serialized format of the instance.

Return type
tuple

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/styledtexttag.html#StyledTextTag.unserialize)[¶](#gramps.gen.lib.styledtexttag.StyledTextTag.unserialize)
Convert a serialized tuple of data to an object.

Parameters
**data** (*tuple*) – Serialized format of instance variables.

### StyledText[¶](#module-gramps.gen.lib.styledtext)
Handling formatted (‘rich text’) strings

*class *`gramps.gen.lib.styledtext.``StyledText`(*text=''*, *tags=None*)[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText)[¶](#gramps.gen.lib.styledtext.StyledText)
Bases: `object`

Helper class to enable character based text formatting.

[`StyledText`](#gramps.gen.lib.styledtext.StyledText) is a wrapper class binding the clear text string and
it’s formatting tags together.

[`StyledText`](#gramps.gen.lib.styledtext.StyledText) provides several string methods in order to
manipulate formatted strings, such as [`join()`](#gramps.gen.lib.styledtext.StyledText.join), [`replace()`](#gramps.gen.lib.styledtext.StyledText.replace),
[`split()`](#gramps.gen.lib.styledtext.StyledText.split), and also supports the ‘+’ operation (`__add__()`).

To get the clear text of the [`StyledText`](#gramps.gen.lib.styledtext.StyledText) use the built-in
`str()` function. To get the list of formatting tags use the
[`get_tags()`](#gramps.gen.lib.styledtext.StyledText.get_tags) method.

StyledText supports the *creation* of formatted texts too. This feature
is intended to replace (or extend) the current report interface.
To be continued… FIXME

Variables

- [**string**](#gramps.gen.lib.grampstype.GrampsType.string) – (str) The clear text part.

- [**tags**](#gramps.gen.lib.styledtext.StyledText.tags) – (list of [`StyledTextTag`](#gramps.gen.lib.styledtexttag.StyledTextTag)) Text tags holding
formatting information for the string.

- [**POS_TEXT**](#gramps.gen.lib.styledtext.StyledText.POS_TEXT) – Position of *string* attribute in the serialized format of
an instance.

- [**POS_TAGS**](#gramps.gen.lib.styledtext.StyledText.POS_TAGS) – (int) Position of *tags* attribute in the serialized format
of an instance.

Warning

The POS_ class variables reflect the serialized object,
they have to be updated in case the data structure or the
[`serialize()`](#gramps.gen.lib.styledtext.StyledText.serialize) method changes!

Note

- There is no sanity check of tags in `__init__()`, because when a
[`StyledText`](#gramps.gen.lib.styledtext.StyledText) is displayed it is passed to a
[`StyledTextBuffer`](../coregui/gui_widgets.html#gramps.gui.widgets.styledtextbuffer.StyledTextBuffer), which in turn will ‘eat’ all invalid
tags (including out-of-range tags too).

- After string methods the tags can become fragmented. That means the same
tag may appear more than once in the tag list with different ranges.
There could be a ‘merge_tags’ functionality in `__init__()`,
however `StyledTextBuffer` will merge them automatically if
the text is displayed.

- Warning: Some of these operations modify the source tag ranges in place
so if you intend to use a source tag more than once, copy it for use.

`POS_TAGS`* = 1*[¶](#gramps.gen.lib.styledtext.StyledText.POS_TAGS)

`POS_TEXT`* = 0*[¶](#gramps.gen.lib.styledtext.StyledText.POS_TEXT)

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.get_schema)[¶](#gramps.gen.lib.styledtext.StyledText.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_string`()[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.get_string)[¶](#gramps.gen.lib.styledtext.StyledText.get_string)
Accessor for the associated string.

`get_tags`()[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.get_tags)[¶](#gramps.gen.lib.styledtext.StyledText.get_tags)
Return the list of formatting tags.

Returns
The formatting tags applied on the text.

Return type
list of 0 or more [`StyledTextTag`](#gramps.gen.lib.styledtexttag.StyledTextTag) instances.

`join`(*seq*)[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.join)[¶](#gramps.gen.lib.styledtext.StyledText.join)
Emulate `__builtin__.str.join()` method.

Parameters
**seq** (basestring or [`StyledText`](#gramps.gen.lib.styledtext.StyledText)) – list of strings to join

Returns
joined strings

Return type
[`StyledText`](#gramps.gen.lib.styledtext.StyledText)

`replace`(*old*, *new*, *count=-1*)[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.replace)[¶](#gramps.gen.lib.styledtext.StyledText.replace)
Emulate `__builtin__.str.replace()` method.

Parameters

- **old** (basestring or [`StyledText`](#gramps.gen.lib.styledtext.StyledText)) – substring to be replaced

- **new** ([`StyledText`](#gramps.gen.lib.styledtext.StyledText)) – substring to replace by

- **count** (*int*) – if given, only the first count occurrences are replaced

Returns
copy of the string with replaced substring(s)

Return type
[`StyledText`](#gramps.gen.lib.styledtext.StyledText)

Warning

by the correct implementation parameter *new* should be
[`StyledText`](#gramps.gen.lib.styledtext.StyledText) or basestring, however only
[`StyledText`](#gramps.gen.lib.styledtext.StyledText) is currently supported.

`serialize`()[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.serialize)[¶](#gramps.gen.lib.styledtext.StyledText.serialize)
Convert the object to a serialized tuple of data.

Returns
Serialized format of the instance.

Return type
tuple

`set_string`(*string*)[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.set_string)[¶](#gramps.gen.lib.styledtext.StyledText.set_string)
Setter for the associated string.

`set_tags`(*tags*)[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.set_tags)[¶](#gramps.gen.lib.styledtext.StyledText.set_tags)
Set the list of formatting tags.

Parameters
**tags** (list of 0 or more [`StyledTextTag`](#gramps.gen.lib.styledtexttag.StyledTextTag) instances.) – The formatting tags applied on the text.

`split`(*sep=None*, *maxsplit=-1*)[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.split)[¶](#gramps.gen.lib.styledtext.StyledText.split)
Emulate `__builtin__.str.split()` method.

Parameters

- **sep** – the delimiter string

- **maxsplit** (*int*) – if given, at most maxsplit splits are done

Returns
a list of the words in the string

Return type
list of [`StyledText`](#gramps.gen.lib.styledtext.StyledText)

`string`[¶](#gramps.gen.lib.styledtext.StyledText.string)
Accessor for the associated string.

`tags`[¶](#gramps.gen.lib.styledtext.StyledText.tags)
Return the list of formatting tags.

Returns
The formatting tags applied on the text.

Return type
list of 0 or more [`StyledTextTag`](#gramps.gen.lib.styledtexttag.StyledTextTag) instances.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/styledtext.html#StyledText.unserialize)[¶](#gramps.gen.lib.styledtext.StyledText.unserialize)
Convert a serialized tuple of data to an object.

Parameters
**data** (*tuple*) – Serialized format of instance variables.

## Meta data[¶](#meta-data)

### GenderStats[¶](#module-gramps.gen.lib.genderstats)
Gender statistics kept in Gramps database.

*class *`gramps.gen.lib.genderstats.``GenderStats`(*stats=None*)[[source]](../_modules/gramps/gen/lib/genderstats.html#GenderStats)[¶](#gramps.gen.lib.genderstats.GenderStats)
Bases: `object`

Class for keeping track of statistics related to Given Name vs. Gender.

This allows the tracking of the liklihood of a person’s given name
indicating the gender of the person.

`clear_stats`()[[source]](../_modules/gramps/gen/lib/genderstats.html#GenderStats.clear_stats)[¶](#gramps.gen.lib.genderstats.GenderStats.clear_stats)

`count_name`(*name*, *gender*)[[source]](../_modules/gramps/gen/lib/genderstats.html#GenderStats.count_name)[¶](#gramps.gen.lib.genderstats.GenderStats.count_name)
Count a given name under gender in the gender stats.

`count_person`(*person*, *undo=0*)[[source]](../_modules/gramps/gen/lib/genderstats.html#GenderStats.count_person)[¶](#gramps.gen.lib.genderstats.GenderStats.count_person)

`guess_gender`(*name*)[[source]](../_modules/gramps/gen/lib/genderstats.html#GenderStats.guess_gender)[¶](#gramps.gen.lib.genderstats.GenderStats.guess_gender)

`name_stats`(*name*)[[source]](../_modules/gramps/gen/lib/genderstats.html#GenderStats.name_stats)[¶](#gramps.gen.lib.genderstats.GenderStats.name_stats)

`save_stats`()[[source]](../_modules/gramps/gen/lib/genderstats.html#GenderStats.save_stats)[¶](#gramps.gen.lib.genderstats.GenderStats.save_stats)

`uncount_person`(*person*)[[source]](../_modules/gramps/gen/lib/genderstats.html#GenderStats.uncount_person)[¶](#gramps.gen.lib.genderstats.GenderStats.uncount_person)

### Researcher[¶](#module-gramps.gen.lib.researcher)
Researcher information for Gramps.

*class *`gramps.gen.lib.researcher.``Researcher`(*source=None*)[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher)[¶](#gramps.gen.lib.researcher.Researcher)
Bases: [`gramps.gen.lib.locationbase.LocationBase`](#gramps.gen.lib.locationbase.LocationBase)

Contains the information about the owner of the database.

`get`()[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.get)[¶](#gramps.gen.lib.researcher.Researcher.get)

`get_address`()[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.get_address)[¶](#gramps.gen.lib.researcher.Researcher.get_address)
Return the database owner’s address.

`get_email`()[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.get_email)[¶](#gramps.gen.lib.researcher.Researcher.get_email)
Return the database owner’s email.

`get_name`()[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.get_name)[¶](#gramps.gen.lib.researcher.Researcher.get_name)
Return the database owner’s name.

`is_empty`()[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.is_empty)[¶](#gramps.gen.lib.researcher.Researcher.is_empty)

`serialize`()[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.serialize)[¶](#gramps.gen.lib.researcher.Researcher.serialize)
Convert the object to a serialized tuple of data.

`set_address`(*data*)[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.set_address)[¶](#gramps.gen.lib.researcher.Researcher.set_address)
Set the database owner’s address.

`set_email`(*data*)[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.set_email)[¶](#gramps.gen.lib.researcher.Researcher.set_email)
Set the database owner’s email.

`set_from`(*other_researcher*)[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.set_from)[¶](#gramps.gen.lib.researcher.Researcher.set_from)
Set all attributes from another instance.

`set_name`(*data*)[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.set_name)[¶](#gramps.gen.lib.researcher.Researcher.set_name)
Set the database owner’s name.

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/researcher.html#Researcher.unserialize)[¶](#gramps.gen.lib.researcher.Researcher.unserialize)
Convert a serialized tuple of data to an object.

## Type classes[¶](#module-gramps.gen.lib.grampstype)
Base type for all gramps types.

*class *`gramps.gen.lib.grampstype.``GrampsTypeMeta`(*name*, *bases*, *namespace*)[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsTypeMeta)[¶](#gramps.gen.lib.grampstype.GrampsTypeMeta)
Bases: `type`

Metaclass for [`GrampsType`](#gramps.gen.lib.grampstype.GrampsType).

Create the class-specific integer/string maps.

### GrampsType[¶](#grampstype)

*class *`gramps.gen.lib.grampstype.``GrampsType`(*value=None*)[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType)[¶](#gramps.gen.lib.grampstype.GrampsType)
Bases: `object`

Base class for all Gramps object types.

Variables

- **_DATAMAP** – (list) 3-tuple like (index, localized_string, english_string).

- **_BLACKLIST** – List of indices to ignore (obsolete/retired entries).
(gramps policy is never to delete type values, or reuse the name (TOKEN)
of any specific type value)

- **POS_** – (int)
Position of attribute in the serialized format of
an instance.

Warning

The POS_ class variables reflect the serialized object,
they have to be updated in case the data structure or the
[`serialize()`](#gramps.gen.lib.grampstype.GrampsType.serialize) method changes!

Variables

- **_CUSTOM** – (int) a custom type object

- **_DEFAULT** – (int) the default type, used on creation

Attribute value
(int) Returns or sets integer value

Attribute string
(str) Returns or sets string value

`POS_STRING`* = 1*[¶](#gramps.gen.lib.grampstype.GrampsType.POS_STRING)

`POS_VALUE`* = 0*[¶](#gramps.gen.lib.grampstype.GrampsType.POS_VALUE)

`get_custom`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.get_custom)[¶](#gramps.gen.lib.grampstype.GrampsType.get_custom)

`get_map`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.get_map)[¶](#gramps.gen.lib.grampstype.GrampsType.get_map)

`get_menu`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.get_menu)[¶](#gramps.gen.lib.grampstype.GrampsType.get_menu)
Return the list of localized names for the menu.

`get_menu_standard_xml`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.get_menu_standard_xml)[¶](#gramps.gen.lib.grampstype.GrampsType.get_menu_standard_xml)
Return the list of XML (english) names for the menu.

*classmethod *`get_schema`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.get_schema)[¶](#gramps.gen.lib.grampstype.GrampsType.get_schema)
Returns the JSON Schema for this class.

Returns
Returns a dict containing the schema.

Return type
dict

`get_standard_names`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.get_standard_names)[¶](#gramps.gen.lib.grampstype.GrampsType.get_standard_names)
Return the list of localized names for all standard types.

`get_standard_xml`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.get_standard_xml)[¶](#gramps.gen.lib.grampstype.GrampsType.get_standard_xml)
Return the list of XML (english) names for all standard types.

`is_custom`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.is_custom)[¶](#gramps.gen.lib.grampstype.GrampsType.is_custom)

`is_default`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.is_default)[¶](#gramps.gen.lib.grampstype.GrampsType.is_default)

`serialize`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.serialize)[¶](#gramps.gen.lib.grampstype.GrampsType.serialize)
Convert the object to a serialized tuple of data.

`set`(*value*)[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.set)[¶](#gramps.gen.lib.grampstype.GrampsType.set)
Set the value/string properties from the passed in value.

`set_from_xml_str`(*value*)[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.set_from_xml_str)[¶](#gramps.gen.lib.grampstype.GrampsType.set_from_xml_str)
This method sets the type instance based on the untranslated string
(obtained e.g. from XML).

`string`[¶](#gramps.gen.lib.grampstype.GrampsType.string)
Returns or sets string value

`unserialize`(*data*)[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.unserialize)[¶](#gramps.gen.lib.grampstype.GrampsType.unserialize)
Convert a serialized tuple of data to an object.

`value`[¶](#gramps.gen.lib.grampstype.GrampsType.value)
Returns or sets integer value

`xml_str`()[[source]](../_modules/gramps/gen/lib/grampstype.html#GrampsType.xml_str)[¶](#gramps.gen.lib.grampstype.GrampsType.xml_str)
Return the untranslated string (e.g. suitable for XML) corresponding
to the type.

### AttributeType[¶](#module-gramps.gen.lib.attrtype)
Provide the different Attribute Types for Gramps.

*class *`gramps.gen.lib.attrtype.``AttributeType`(*value=None*)[[source]](../_modules/gramps/gen/lib/attrtype.html#AttributeType)[¶](#gramps.gen.lib.attrtype.AttributeType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

`AGE`* = 10*[¶](#gramps.gen.lib.attrtype.AttributeType.AGE)

`AGENCY`* = 9*[¶](#gramps.gen.lib.attrtype.AttributeType.AGENCY)

`CASTE`* = 1*[¶](#gramps.gen.lib.attrtype.AttributeType.CASTE)

`CAUSE`* = 8*[¶](#gramps.gen.lib.attrtype.AttributeType.CAUSE)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.attrtype.AttributeType.CUSTOM)

`DESCRIPTION`* = 2*[¶](#gramps.gen.lib.attrtype.AttributeType.DESCRIPTION)

`FATHER_AGE`* = 11*[¶](#gramps.gen.lib.attrtype.AttributeType.FATHER_AGE)

`ID`* = 3*[¶](#gramps.gen.lib.attrtype.AttributeType.ID)

`MOTHER_AGE`* = 12*[¶](#gramps.gen.lib.attrtype.AttributeType.MOTHER_AGE)

`NATIONAL`* = 4*[¶](#gramps.gen.lib.attrtype.AttributeType.NATIONAL)

`NICKNAME`* = 7*[¶](#gramps.gen.lib.attrtype.AttributeType.NICKNAME)

`NUM_CHILD`* = 5*[¶](#gramps.gen.lib.attrtype.AttributeType.NUM_CHILD)

`OCCUPATION`* = 15*[¶](#gramps.gen.lib.attrtype.AttributeType.OCCUPATION)

`SSN`* = 6*[¶](#gramps.gen.lib.attrtype.AttributeType.SSN)

`TIME`* = 14*[¶](#gramps.gen.lib.attrtype.AttributeType.TIME)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.attrtype.AttributeType.UNKNOWN)

`WITNESS`* = 13*[¶](#gramps.gen.lib.attrtype.AttributeType.WITNESS)

`type2base`()[[source]](../_modules/gramps/gen/lib/attrtype.html#AttributeType.type2base)[¶](#gramps.gen.lib.attrtype.AttributeType.type2base)
Return the untranslated string suitable for UI (once translated).

### ChildRefType[¶](#module-gramps.gen.lib.childreftype)
Provide the different child reference types.

*class *`gramps.gen.lib.childreftype.``ChildRefType`(*value=None*)[[source]](../_modules/gramps/gen/lib/childreftype.html#ChildRefType)[¶](#gramps.gen.lib.childreftype.ChildRefType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

Provide the different ChildRef types.

`ADOPTED`* = 2*[¶](#gramps.gen.lib.childreftype.ChildRefType.ADOPTED)

`BIRTH`* = 1*[¶](#gramps.gen.lib.childreftype.ChildRefType.BIRTH)

`CUSTOM`* = 7*[¶](#gramps.gen.lib.childreftype.ChildRefType.CUSTOM)

`FOSTER`* = 5*[¶](#gramps.gen.lib.childreftype.ChildRefType.FOSTER)

`NONE`* = 0*[¶](#gramps.gen.lib.childreftype.ChildRefType.NONE)

`SPONSORED`* = 4*[¶](#gramps.gen.lib.childreftype.ChildRefType.SPONSORED)

`STEPCHILD`* = 3*[¶](#gramps.gen.lib.childreftype.ChildRefType.STEPCHILD)

`UNKNOWN`* = 6*[¶](#gramps.gen.lib.childreftype.ChildRefType.UNKNOWN)

### EventType[¶](#module-gramps.gen.lib.eventtype)
Provide the different event types

*class *`gramps.gen.lib.eventtype.``EventType`(*value=None*)[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType)[¶](#gramps.gen.lib.eventtype.EventType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

Event types.

`ADOPT`* = 11*[¶](#gramps.gen.lib.eventtype.EventType.ADOPT)

`ADULT_CHRISTEN`* = 14*[¶](#gramps.gen.lib.eventtype.EventType.ADULT_CHRISTEN)

`ANNULMENT`* = 9*[¶](#gramps.gen.lib.eventtype.EventType.ANNULMENT)

`BAPTISM`* = 15*[¶](#gramps.gen.lib.eventtype.EventType.BAPTISM)

`BAR_MITZVAH`* = 16*[¶](#gramps.gen.lib.eventtype.EventType.BAR_MITZVAH)

`BAS_MITZVAH`* = 17*[¶](#gramps.gen.lib.eventtype.EventType.BAS_MITZVAH)

`BIRTH`* = 12*[¶](#gramps.gen.lib.eventtype.EventType.BIRTH)

`BLESS`* = 18*[¶](#gramps.gen.lib.eventtype.EventType.BLESS)

`BURIAL`* = 19*[¶](#gramps.gen.lib.eventtype.EventType.BURIAL)

`CAUSE_DEATH`* = 20*[¶](#gramps.gen.lib.eventtype.EventType.CAUSE_DEATH)

`CENSUS`* = 21*[¶](#gramps.gen.lib.eventtype.EventType.CENSUS)

`CHRISTEN`* = 22*[¶](#gramps.gen.lib.eventtype.EventType.CHRISTEN)

`CONFIRMATION`* = 23*[¶](#gramps.gen.lib.eventtype.EventType.CONFIRMATION)

`CREMATION`* = 24*[¶](#gramps.gen.lib.eventtype.EventType.CREMATION)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.eventtype.EventType.CUSTOM)

`DEATH`* = 13*[¶](#gramps.gen.lib.eventtype.EventType.DEATH)

`DEGREE`* = 25*[¶](#gramps.gen.lib.eventtype.EventType.DEGREE)

`DIVORCE`* = 7*[¶](#gramps.gen.lib.eventtype.EventType.DIVORCE)

`DIV_FILING`* = 8*[¶](#gramps.gen.lib.eventtype.EventType.DIV_FILING)

`EDUCATION`* = 26*[¶](#gramps.gen.lib.eventtype.EventType.EDUCATION)

`ELECTED`* = 27*[¶](#gramps.gen.lib.eventtype.EventType.ELECTED)

`EMIGRATION`* = 28*[¶](#gramps.gen.lib.eventtype.EventType.EMIGRATION)

`ENGAGEMENT`* = 6*[¶](#gramps.gen.lib.eventtype.EventType.ENGAGEMENT)

`FIRST_COMMUN`* = 29*[¶](#gramps.gen.lib.eventtype.EventType.FIRST_COMMUN)

`GRADUATION`* = 31*[¶](#gramps.gen.lib.eventtype.EventType.GRADUATION)

`IMMIGRATION`* = 30*[¶](#gramps.gen.lib.eventtype.EventType.IMMIGRATION)

`MARRIAGE`* = 1*[¶](#gramps.gen.lib.eventtype.EventType.MARRIAGE)

`MARR_ALT`* = 10*[¶](#gramps.gen.lib.eventtype.EventType.MARR_ALT)

`MARR_BANNS`* = 5*[¶](#gramps.gen.lib.eventtype.EventType.MARR_BANNS)

`MARR_CONTR`* = 4*[¶](#gramps.gen.lib.eventtype.EventType.MARR_CONTR)

`MARR_LIC`* = 3*[¶](#gramps.gen.lib.eventtype.EventType.MARR_LIC)

`MARR_SETTL`* = 2*[¶](#gramps.gen.lib.eventtype.EventType.MARR_SETTL)

`MED_INFO`* = 32*[¶](#gramps.gen.lib.eventtype.EventType.MED_INFO)

`MILITARY_SERV`* = 33*[¶](#gramps.gen.lib.eventtype.EventType.MILITARY_SERV)

`NATURALIZATION`* = 34*[¶](#gramps.gen.lib.eventtype.EventType.NATURALIZATION)

`NOB_TITLE`* = 35*[¶](#gramps.gen.lib.eventtype.EventType.NOB_TITLE)

`NUM_MARRIAGES`* = 36*[¶](#gramps.gen.lib.eventtype.EventType.NUM_MARRIAGES)

`OCCUPATION`* = 37*[¶](#gramps.gen.lib.eventtype.EventType.OCCUPATION)

`ORDINATION`* = 38*[¶](#gramps.gen.lib.eventtype.EventType.ORDINATION)

`PROBATE`* = 39*[¶](#gramps.gen.lib.eventtype.EventType.PROBATE)

`PROPERTY`* = 40*[¶](#gramps.gen.lib.eventtype.EventType.PROPERTY)

`RELIGION`* = 41*[¶](#gramps.gen.lib.eventtype.EventType.RELIGION)

`RESIDENCE`* = 42*[¶](#gramps.gen.lib.eventtype.EventType.RESIDENCE)

`RETIREMENT`* = 43*[¶](#gramps.gen.lib.eventtype.EventType.RETIREMENT)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.eventtype.EventType.UNKNOWN)

`WILL`* = 44*[¶](#gramps.gen.lib.eventtype.EventType.WILL)

`get_abbreviation`(*trans_text=>*)[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.get_abbreviation)[¶](#gramps.gen.lib.eventtype.EventType.get_abbreviation)
Returns the abbreviation for this event. Uses the explicitly
given abbreviations, or first letter of each word, or the first
three letters. Appends a period after the abbreviation,
but not if string is in _ABBREVIATIONS.

If trans_text is passed in (a GrampsLocale sgettext instance)
then the translated abbreviation will be returned instead.

`is_baptism`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_baptism)[¶](#gramps.gen.lib.eventtype.EventType.is_baptism)
Returns True if EventType is BAPTISM, False
otherwise.

`is_birth`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_birth)[¶](#gramps.gen.lib.eventtype.EventType.is_birth)
Returns True if EventType is BIRTH, False
otherwise.

`is_birth_fallback`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_birth_fallback)[¶](#gramps.gen.lib.eventtype.EventType.is_birth_fallback)
Returns True if EventType is a birth fallback, False
otherwise.

`is_burial`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_burial)[¶](#gramps.gen.lib.eventtype.EventType.is_burial)
Returns True if EventType is BURIAL, False
otherwise.

`is_death`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_death)[¶](#gramps.gen.lib.eventtype.EventType.is_death)
Returns True if EventType is DEATH, False
otherwise.

`is_death_fallback`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_death_fallback)[¶](#gramps.gen.lib.eventtype.EventType.is_death_fallback)
Returns True if EventType is a death fallback, False
otherwise.

`is_divorce`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_divorce)[¶](#gramps.gen.lib.eventtype.EventType.is_divorce)
Returns True if EventType is DIVORCE, False otherwise.

`is_divorce_fallback`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_divorce_fallback)[¶](#gramps.gen.lib.eventtype.EventType.is_divorce_fallback)
Returns True if EventType is a divorce fallback, False
otherwise.

`is_marriage`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_marriage)[¶](#gramps.gen.lib.eventtype.EventType.is_marriage)
Returns True if EventType is MARRIAGE, False otherwise.

`is_marriage_fallback`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_marriage_fallback)[¶](#gramps.gen.lib.eventtype.EventType.is_marriage_fallback)
Returns True if EventType is a marriage fallback, False
otherwise.

`is_relationship_event`()[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_relationship_event)[¶](#gramps.gen.lib.eventtype.EventType.is_relationship_event)
Returns True is EventType is a relationship type event.

`is_type`(*event_name*)[[source]](../_modules/gramps/gen/lib/eventtype.html#EventType.is_type)[¶](#gramps.gen.lib.eventtype.EventType.is_type)
Returns True if EventType has name EVENT_NAME, False otherwise.

### EventRoleType[¶](#module-gramps.gen.lib.eventroletype)
Provide the different event roles.

*class *`gramps.gen.lib.eventroletype.``EventRoleType`(*value=None*)[[source]](../_modules/gramps/gen/lib/eventroletype.html#EventRoleType)[¶](#gramps.gen.lib.eventroletype.EventRoleType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

`AIDE`* = 4*[¶](#gramps.gen.lib.eventroletype.EventRoleType.AIDE)

`BRIDE`* = 5*[¶](#gramps.gen.lib.eventroletype.EventRoleType.BRIDE)

`CELEBRANT`* = 3*[¶](#gramps.gen.lib.eventroletype.EventRoleType.CELEBRANT)

`CLERGY`* = 2*[¶](#gramps.gen.lib.eventroletype.EventRoleType.CLERGY)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.eventroletype.EventRoleType.CUSTOM)

`FAMILY`* = 8*[¶](#gramps.gen.lib.eventroletype.EventRoleType.FAMILY)

`GROOM`* = 6*[¶](#gramps.gen.lib.eventroletype.EventRoleType.GROOM)

`INFORMANT`* = 9*[¶](#gramps.gen.lib.eventroletype.EventRoleType.INFORMANT)

`PRIMARY`* = 1*[¶](#gramps.gen.lib.eventroletype.EventRoleType.PRIMARY)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.eventroletype.EventRoleType.UNKNOWN)

`WITNESS`* = 7*[¶](#gramps.gen.lib.eventroletype.EventRoleType.WITNESS)

`is_family`()[[source]](../_modules/gramps/gen/lib/eventroletype.html#EventRoleType.is_family)[¶](#gramps.gen.lib.eventroletype.EventRoleType.is_family)
Returns True if EventRoleType is FAMILY, False otherwise.

`is_primary`()[[source]](../_modules/gramps/gen/lib/eventroletype.html#EventRoleType.is_primary)[¶](#gramps.gen.lib.eventroletype.EventRoleType.is_primary)
Returns True if EventRoleType is PRIMARY, False otherwise.

### FamilyRelType[¶](#module-gramps.gen.lib.familyreltype)
Provide the different family reference types.

*class *`gramps.gen.lib.familyreltype.``FamilyRelType`(*value=None*)[[source]](../_modules/gramps/gen/lib/familyreltype.html#FamilyRelType)[¶](#gramps.gen.lib.familyreltype.FamilyRelType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

`CIVIL_UNION`* = 2*[¶](#gramps.gen.lib.familyreltype.FamilyRelType.CIVIL_UNION)

`CUSTOM`* = 4*[¶](#gramps.gen.lib.familyreltype.FamilyRelType.CUSTOM)

`MARRIED`* = 0*[¶](#gramps.gen.lib.familyreltype.FamilyRelType.MARRIED)

`UNKNOWN`* = 3*[¶](#gramps.gen.lib.familyreltype.FamilyRelType.UNKNOWN)

`UNMARRIED`* = 1*[¶](#gramps.gen.lib.familyreltype.FamilyRelType.UNMARRIED)

### MarkerType[¶](#module-gramps.gen.lib.markertype)
Marker types.

From version 3.3 onwards, this is only kept to convert markers into tags
when loading old database files.

*class *`gramps.gen.lib.markertype.``MarkerType`(*value=None*)[[source]](../_modules/gramps/gen/lib/markertype.html#MarkerType)[¶](#gramps.gen.lib.markertype.MarkerType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

Class for handling data markers.

`COMPLETE`* = 1*[¶](#gramps.gen.lib.markertype.MarkerType.COMPLETE)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.markertype.MarkerType.CUSTOM)

`NONE`* = -1*[¶](#gramps.gen.lib.markertype.MarkerType.NONE)

`TODO_TYPE`* = 2*[¶](#gramps.gen.lib.markertype.MarkerType.TODO_TYPE)

### NameType[¶](#module-gramps.gen.lib.nametype)
Name types.

*class *`gramps.gen.lib.nametype.``NameType`(*value=None*)[[source]](../_modules/gramps/gen/lib/nametype.html#NameType)[¶](#gramps.gen.lib.nametype.NameType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

`AKA`* = 1*[¶](#gramps.gen.lib.nametype.NameType.AKA)

`BIRTH`* = 2*[¶](#gramps.gen.lib.nametype.NameType.BIRTH)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.nametype.NameType.CUSTOM)

`MARRIED`* = 3*[¶](#gramps.gen.lib.nametype.NameType.MARRIED)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.nametype.NameType.UNKNOWN)

### NameOriginType[¶](#module-gramps.gen.lib.nameorigintype)
Name types.

*class *`gramps.gen.lib.nameorigintype.``NameOriginType`(*value=None*)[[source]](../_modules/gramps/gen/lib/nameorigintype.html#NameOriginType)[¶](#gramps.gen.lib.nameorigintype.NameOriginType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

Name Origin Types

`CUSTOM`* = 0*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.CUSTOM)

`FEUDAL`* = 7*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.FEUDAL)

`GIVEN`* = 3*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.GIVEN)

`INHERITED`* = 2*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.INHERITED)

`LOCATION`* = 12*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.LOCATION)

`MATRILINEAL`* = 10*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.MATRILINEAL)

`MATRONYMIC`* = 6*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.MATRONYMIC)

`NONE`* = 1*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.NONE)

`OCCUPATION`* = 11*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.OCCUPATION)

`PATRILINEAL`* = 9*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.PATRILINEAL)

`PATRONYMIC`* = 5*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.PATRONYMIC)

`PSEUDONYM`* = 8*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.PSEUDONYM)

`TAKEN`* = 4*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.TAKEN)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.nameorigintype.NameOriginType.UNKNOWN)

### NoteType[¶](#module-gramps.gen.lib.notetype)
Note types.

*class *`gramps.gen.lib.notetype.``NoteType`(*value=None*)[[source]](../_modules/gramps/gen/lib/notetype.html#NoteType)[¶](#gramps.gen.lib.notetype.NoteType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

`ADDRESS`* = 6*[¶](#gramps.gen.lib.notetype.NoteType.ADDRESS)

`ASSOCIATION`* = 7*[¶](#gramps.gen.lib.notetype.NoteType.ASSOCIATION)

`ATTRIBUTE`* = 5*[¶](#gramps.gen.lib.notetype.NoteType.ATTRIBUTE)

`CHILDREF`* = 19*[¶](#gramps.gen.lib.notetype.NoteType.CHILDREF)

`CITATION`* = 22*[¶](#gramps.gen.lib.notetype.NoteType.CITATION)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.notetype.NoteType.CUSTOM)

`EVENT`* = 10*[¶](#gramps.gen.lib.notetype.NoteType.EVENT)

`EVENTREF`* = 11*[¶](#gramps.gen.lib.notetype.NoteType.EVENTREF)

`FAMILY`* = 9*[¶](#gramps.gen.lib.notetype.NoteType.FAMILY)

`GENERAL`* = 1*[¶](#gramps.gen.lib.notetype.NoteType.GENERAL)

`HTML_CODE`* = 24*[¶](#gramps.gen.lib.notetype.NoteType.HTML_CODE)

`LDS`* = 8*[¶](#gramps.gen.lib.notetype.NoteType.LDS)

`LINK`* = 26*[¶](#gramps.gen.lib.notetype.NoteType.LINK)

`MEDIA`* = 17*[¶](#gramps.gen.lib.notetype.NoteType.MEDIA)

`MEDIAREF`* = 18*[¶](#gramps.gen.lib.notetype.NoteType.MEDIAREF)

`PERSON`* = 4*[¶](#gramps.gen.lib.notetype.NoteType.PERSON)

`PERSONNAME`* = 20*[¶](#gramps.gen.lib.notetype.NoteType.PERSONNAME)

`PLACE`* = 14*[¶](#gramps.gen.lib.notetype.NoteType.PLACE)

`REPO`* = 15*[¶](#gramps.gen.lib.notetype.NoteType.REPO)

`REPOREF`* = 16*[¶](#gramps.gen.lib.notetype.NoteType.REPOREF)

`REPORT_TEXT`* = 23*[¶](#gramps.gen.lib.notetype.NoteType.REPORT_TEXT)

`RESEARCH`* = 2*[¶](#gramps.gen.lib.notetype.NoteType.RESEARCH)

`SOURCE`* = 12*[¶](#gramps.gen.lib.notetype.NoteType.SOURCE)

`SOURCEREF`* = 13*[¶](#gramps.gen.lib.notetype.NoteType.SOURCEREF)

`SOURCE_TEXT`* = 21*[¶](#gramps.gen.lib.notetype.NoteType.SOURCE_TEXT)

`TODO`* = 25*[¶](#gramps.gen.lib.notetype.NoteType.TODO)

`TRANSCRIPT`* = 3*[¶](#gramps.gen.lib.notetype.NoteType.TRANSCRIPT)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.notetype.NoteType.UNKNOWN)

`get_ignore_list`(*exception*)[[source]](../_modules/gramps/gen/lib/notetype.html#NoteType.get_ignore_list)[¶](#gramps.gen.lib.notetype.NoteType.get_ignore_list)
Return a list of the types to ignore and not include in default lists.

Exception is a sublist of types that may not be ignored

Parameters
**exception** (*list*) – list of integer values corresponding with types that
have to be excluded from the ignore list

Returns
list of integers corresponding with the types to ignore when
showing a list of different types

Return type
list

### PlaceType[¶](#module-gramps.gen.lib.placetype)
Provide the different place types.

*class *`gramps.gen.lib.placetype.``PlaceType`(*value=None*)[[source]](../_modules/gramps/gen/lib/placetype.html#PlaceType)[¶](#gramps.gen.lib.placetype.PlaceType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

`BOROUGH`* = 13*[¶](#gramps.gen.lib.placetype.PlaceType.BOROUGH)

`BUILDING`* = 19*[¶](#gramps.gen.lib.placetype.PlaceType.BUILDING)

`CITY`* = 4*[¶](#gramps.gen.lib.placetype.PlaceType.CITY)

`COUNTRY`* = 1*[¶](#gramps.gen.lib.placetype.PlaceType.COUNTRY)

`COUNTY`* = 3*[¶](#gramps.gen.lib.placetype.PlaceType.COUNTY)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.placetype.PlaceType.CUSTOM)

`DEPARTMENT`* = 10*[¶](#gramps.gen.lib.placetype.PlaceType.DEPARTMENT)

`DISTRICT`* = 12*[¶](#gramps.gen.lib.placetype.PlaceType.DISTRICT)

`FARM`* = 18*[¶](#gramps.gen.lib.placetype.PlaceType.FARM)

`HAMLET`* = 17*[¶](#gramps.gen.lib.placetype.PlaceType.HAMLET)

`LOCALITY`* = 6*[¶](#gramps.gen.lib.placetype.PlaceType.LOCALITY)

`MUNICIPALITY`* = 14*[¶](#gramps.gen.lib.placetype.PlaceType.MUNICIPALITY)

`NEIGHBORHOOD`* = 11*[¶](#gramps.gen.lib.placetype.PlaceType.NEIGHBORHOOD)

`NUMBER`* = 20*[¶](#gramps.gen.lib.placetype.PlaceType.NUMBER)

`PARISH`* = 5*[¶](#gramps.gen.lib.placetype.PlaceType.PARISH)

`PROVINCE`* = 8*[¶](#gramps.gen.lib.placetype.PlaceType.PROVINCE)

`REGION`* = 9*[¶](#gramps.gen.lib.placetype.PlaceType.REGION)

`STATE`* = 2*[¶](#gramps.gen.lib.placetype.PlaceType.STATE)

`STREET`* = 7*[¶](#gramps.gen.lib.placetype.PlaceType.STREET)

`TOWN`* = 15*[¶](#gramps.gen.lib.placetype.PlaceType.TOWN)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.placetype.PlaceType.UNKNOWN)

`VILLAGE`* = 16*[¶](#gramps.gen.lib.placetype.PlaceType.VILLAGE)

### RepositoryType[¶](#module-gramps.gen.lib.repotype)
Repository types.

*class *`gramps.gen.lib.repotype.``RepositoryType`(*value=None*)[[source]](../_modules/gramps/gen/lib/repotype.html#RepositoryType)[¶](#gramps.gen.lib.repotype.RepositoryType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

`ALBUM`* = 5*[¶](#gramps.gen.lib.repotype.RepositoryType.ALBUM)

`ARCHIVE`* = 4*[¶](#gramps.gen.lib.repotype.RepositoryType.ARCHIVE)

`BOOKSTORE`* = 7*[¶](#gramps.gen.lib.repotype.RepositoryType.BOOKSTORE)

`CEMETERY`* = 2*[¶](#gramps.gen.lib.repotype.RepositoryType.CEMETERY)

`CHURCH`* = 3*[¶](#gramps.gen.lib.repotype.RepositoryType.CHURCH)

`COLLECTION`* = 8*[¶](#gramps.gen.lib.repotype.RepositoryType.COLLECTION)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.repotype.RepositoryType.CUSTOM)

`LIBRARY`* = 1*[¶](#gramps.gen.lib.repotype.RepositoryType.LIBRARY)

`SAFE`* = 9*[¶](#gramps.gen.lib.repotype.RepositoryType.SAFE)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.repotype.RepositoryType.UNKNOWN)

`WEBSITE`* = 6*[¶](#gramps.gen.lib.repotype.RepositoryType.WEBSITE)

### SourceMediaType[¶](#module-gramps.gen.lib.srcmediatype)
SourceMedia types.

*class *`gramps.gen.lib.srcmediatype.``SourceMediaType`(*value=None*)[[source]](../_modules/gramps/gen/lib/srcmediatype.html#SourceMediaType)[¶](#gramps.gen.lib.srcmediatype.SourceMediaType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

`AUDIO`* = 1*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.AUDIO)

`BOOK`* = 2*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.BOOK)

`CARD`* = 3*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.CARD)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.CUSTOM)

`ELECTRONIC`* = 4*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.ELECTRONIC)

`FICHE`* = 5*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.FICHE)

`FILM`* = 6*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.FILM)

`MAGAZINE`* = 7*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.MAGAZINE)

`MANUSCRIPT`* = 8*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.MANUSCRIPT)

`MAP`* = 9*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.MAP)

`NEWSPAPER`* = 10*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.NEWSPAPER)

`PHOTO`* = 11*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.PHOTO)

`TOMBSTONE`* = 12*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.TOMBSTONE)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.UNKNOWN)

`VIDEO`* = 13*[¶](#gramps.gen.lib.srcmediatype.SourceMediaType.VIDEO)

### StyledTextTagType[¶](#module-gramps.gen.lib.styledtexttagtype)
Define text formatting tag types.

*class *`gramps.gen.lib.styledtexttagtype.``StyledTextTagType`(*value=None*)[[source]](../_modules/gramps/gen/lib/styledtexttagtype.html#StyledTextTagType)[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

Text formatting tag type definition.

Here we only define new class variables. For details see
`GrampsType`.

`BOLD`* = 0*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.BOLD)

`FONTCOLOR`* = 5*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.FONTCOLOR)

`FONTFACE`* = 3*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.FONTFACE)

`FONTSIZE`* = 4*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.FONTSIZE)

`HIGHLIGHT`* = 6*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.HIGHLIGHT)

`ITALIC`* = 1*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.ITALIC)

`LINK`* = 8*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.LINK)

`NONE_TYPE`* = -1*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.NONE_TYPE)

`STYLE_DEFAULT`* = {0: False, 1: False, 2: False, 3: 'Sans', 4: 10, 5: '#000000', 6: '#FFFFFF', 7: False, 8: ''}*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.STYLE_DEFAULT)

`STYLE_TYPE`* = {0: , 1: , 2: , 3: , 4: , 5: , 6: , 7: , 8: }*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.STYLE_TYPE)

`SUPERSCRIPT`* = 7*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.SUPERSCRIPT)

`UNDERLINE`* = 2*[¶](#gramps.gen.lib.styledtexttagtype.StyledTextTagType.UNDERLINE)

### UrlType[¶](#module-gramps.gen.lib.urltype)
URL types

*class *`gramps.gen.lib.urltype.``UrlType`(*value=None*)[[source]](../_modules/gramps/gen/lib/urltype.html#UrlType)[¶](#gramps.gen.lib.urltype.UrlType)
Bases: [`gramps.gen.lib.grampstype.GrampsType`](#gramps.gen.lib.grampstype.GrampsType)

`CUSTOM`* = 0*[¶](#gramps.gen.lib.urltype.UrlType.CUSTOM)

`EMAIL`* = 1*[¶](#gramps.gen.lib.urltype.UrlType.EMAIL)

`UNKNOWN`* = -1*[¶](#gramps.gen.lib.urltype.UrlType.UNKNOWN)

`WEB_FTP`* = 4*[¶](#gramps.gen.lib.urltype.UrlType.WEB_FTP)

`WEB_HOME`* = 2*[¶](#gramps.gen.lib.urltype.UrlType.WEB_HOME)

`WEB_SEARCH`* = 3*[¶](#gramps.gen.lib.urltype.UrlType.WEB_SEARCH)

 ### [Table of Contents](../index.html)

- [The `gramps.gen.lib` Module](#)

[Base objects](#base-objects)

[BaseObject](#module-gramps.gen.lib.baseobj)
- [AddressBase](#module-gramps.gen.lib.addressbase)
- [AttributeRootBase](#module-gramps.gen.lib.attrbase)
- [AttributeBase](#attributebase)
- [SrcAttributeBase](#srcattributebase)
- [CitationBase](#module-gramps.gen.lib.citationbase)
- [IndirectCitationBase](#indirectcitationbase)
- [DateBase](#module-gramps.gen.lib.datebase)
- [LdsOrdBase](#module-gramps.gen.lib.ldsordbase)
- [LocationBase](#module-gramps.gen.lib.locationbase)
- [MediaBase](#module-gramps.gen.lib.mediabase)
- [NoteBase](#module-gramps.gen.lib.notebase)
- [PlaceBase](#module-gramps.gen.lib.placebase)
- [PrivacyBase](#module-gramps.gen.lib.privacybase)
- [RefBase](#module-gramps.gen.lib.refbase)
- [SurnameBase](#module-gramps.gen.lib.surnamebase)
- [TagBase](#module-gramps.gen.lib.tagbase)
- [UrlBase](#module-gramps.gen.lib.urlbase)

- [Primary objects](#primary-objects)

[BasicPrimaryObject](#module-gramps.gen.lib.primaryobj)
- [PrimaryObject](#primaryobject)
- [Person](#module-gramps.gen.lib.person)
- [Family](#module-gramps.gen.lib.family)
- [Event](#module-gramps.gen.lib.event)
- [Place](#module-gramps.gen.lib.place)
- [Source](#module-gramps.gen.lib.src)
- [Citation](#module-gramps.gen.lib.citation)
- [Media](#module-gramps.gen.lib.media)
- [Repository](#module-gramps.gen.lib.repo)
- [Note](#module-gramps.gen.lib.note)

- [Secondary objects](#secondary-objects)

[Secondary Object](#module-gramps.gen.lib.secondaryobj)
- [Address](#module-gramps.gen.lib.address)
- [Attribute](#module-gramps.gen.lib.attribute)
- [AttributeRoot](#attributeroot)
- [LdsOrd](#module-gramps.gen.lib.ldsord)
- [Location](#module-gramps.gen.lib.location)
- [Name](#module-gramps.gen.lib.name)
- [Surname](#module-gramps.gen.lib.surname)
- [Url](#module-gramps.gen.lib.url)

- [Reference objects](#reference-objects)

[ChildRef](#module-gramps.gen.lib.childref)
- [EventRef](#module-gramps.gen.lib.eventref)
- [MediaRef](#module-gramps.gen.lib.mediaref)
- [PersonRef](#module-gramps.gen.lib.personref)
- [PlaceRef](#module-gramps.gen.lib.placeref)
- [RepoRef](#module-gramps.gen.lib.reporef)

- [Table objects](#table-objects)

[Table object](#module-gramps.gen.lib.tableobj)
- [Tag](#module-gramps.gen.lib.tag)

- [Date objects](#module-gramps.gen.lib.date)

[Date](#date)
- [Span](#span)
- [DateError](#dateerror)

- [Text objects](#text-objects)

[StyledTextTag](#module-gramps.gen.lib.styledtexttag)
- [StyledText](#module-gramps.gen.lib.styledtext)

- [Meta data](#meta-data)

[GenderStats](#module-gramps.gen.lib.genderstats)
- [Researcher](#module-gramps.gen.lib.researcher)

- [Type classes](#module-gramps.gen.lib.grampstype)

[GrampsType](#grampstype)
- [AttributeType](#module-gramps.gen.lib.attrtype)
- [ChildRefType](#module-gramps.gen.lib.childreftype)
- [EventType](#module-gramps.gen.lib.eventtype)
- [EventRoleType](#module-gramps.gen.lib.eventroletype)
- [FamilyRelType](#module-gramps.gen.lib.familyreltype)
- [MarkerType](#module-gramps.gen.lib.markertype)
- [NameType](#module-gramps.gen.lib.nametype)
- [NameOriginType](#module-gramps.gen.lib.nameorigintype)
- [NoteType](#module-gramps.gen.lib.notetype)
- [PlaceType](#module-gramps.gen.lib.placetype)
- [RepositoryType](#module-gramps.gen.lib.repotype)
- [SourceMediaType](#module-gramps.gen.lib.srcmediatype)
- [StyledTextTagType](#module-gramps.gen.lib.styledtexttagtype)
- [UrlType](#module-gramps.gen.lib.urltype)

 #### Previous topic
 [Code Documentation](../api.html)

 #### Next topic
 [The `gramps.gen` Module](gen.html)

 ### This Page

 - [Show Source](../_sources/gen/gen_lib.rst.txt)

 ### Quick search

 © Copyright 2001-2019, The Gramps Project.
 Created using [Sphinx](http://sphinx-doc.org/) 2.0.1.