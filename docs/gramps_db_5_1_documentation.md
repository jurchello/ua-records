# Gramps Database API 5.1.x

**Source:** [https://gramps-project.org/api_5_1_x/gen/gen_db.html](https://gramps-project.org/api_5_1_x/gen/gen_db.html)

## The gramps.gen.db Module

Gramps Database API.

Database Architecture
Access to the database is made through Python classes. Exactly what functionality you have is dependent on the properties of the database. For example, if you are accessing a read-only view, then you will only have access to a subset of the methods available.

At the root of any database interface is either DbReadBase and/or DbWriteBase. These define the methods to read and write to a database, respectively.

The full database hierarchy is:

DbBsddb - read and write implementation to BSDDB databases

DbWriteBase - virtual and implementation-independent methods for reading data

DbBsddbRead - read-only (accessors, getters) implementation to BSDDB databases

DbReadBase - virtual and implementation-independent methods for reading data

Callback - callback and signal functions

UpdateCallback - callback functionality

DbBsddb
The DbBsddb interface defines a hierarchical database (non-relational) written in PyBSDDB. There is no such thing as a database schema, and the meaning of the data is defined in the Python classes above. The data is stored as pickled tuples and unserialized into the primary data types (below).

More details can be found in the manual’s Using database API.

GrampsDbBase
Base class for the Gramps databases. All database interfaces should inherit from this class.

class gramps.gen.db.base.DbReadBase[source]
Bases: object

Gramps database object. This object is a base class for all database interfaces. All methods raise NotImplementedError and must be implemented in the derived class as required.

close()[source]
Close the specified database.

db_has_bm_changes()[source]
Return whethere there were bookmark changes during the session.

find_backlink_handles(handle, include_classes=None)[source]
Find all objects that hold a reference to the object handle.

Returns an iterator over a list of (class_name, handle) tuples.

Parameters
handle (str database handle) – handle of the object to search for.

include_classes (list of class names) – list of class names to include in the results. Default is None which includes all classes.

This default implementation does a sequential scan through all the primary object databases and is very slow. Backends can override this method to provide much faster implementations that make use of additional capabilities of the backend.

Note that this is a generator function, it returns a iterator for use in loops. If you want a list of the results use:

result_list = list(find_backlink_handles(handle))
find_initial_person()[source]
Returns first person in the database

find_next_citation_gramps_id()[source]
Return the next available Gramps ID for a Event object based off the event ID prefix.

find_next_event_gramps_id()[source]
Return the next available Gramps ID for a Event object based off the event ID prefix.

find_next_family_gramps_id()[source]
Return the next available Gramps ID for a Family object based off the family ID prefix.

find_next_media_gramps_id()[source]
Return the next available Gramps ID for a Media object based off the media object ID prefix.

find_next_note_gramps_id()[source]
Return the next available Gramps ID for a Note object based off the note ID prefix.

find_next_person_gramps_id()[source]
Return the next available Gramps ID for a Person object based off the person ID prefix.

find_next_place_gramps_id()[source]
Return the next available Gramps ID for a Place object based off the place ID prefix.

find_next_repository_gramps_id()[source]
Return the next available Gramps ID for a Repository object based off the repository ID prefix.

find_next_source_gramps_id()[source]
Return the next available Gramps ID for a Source object based off the source ID prefix.

get_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_child_reference_types()[source]
Return a list of all child reference types associated with Family instances in the database.

get_citation_bookmarks()[source]
Return the list of Citation handles in the bookmarks.

get_citation_cursor()[source]
Return a reference to a cursor over Citation objects. Example use:

with get_citation_cursor() as cursor:
    for handle, citation in cursor:
        # process citation object pointed to by the handle
get_citation_from_gramps_id(val)[source]
Find a Citation in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Citation exists, None is returned.

get_citation_from_handle(handle)[source]
Return a Citation in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Citation exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Citation is filtered out.

get_citation_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Citation in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Citation title.

locale (A GrampsLocale object.) – The locale to use for collation.

get_dbid()[source]
A unique ID for this database on this computer.

get_dbname()[source]
A name for this database on this computer.

get_default_handle()[source]
Return the default Person of the database.

get_default_person()[source]
Return the default Person of the database.

get_event_attribute_types()[source]
Return a list of all Attribute types assocated with Event instances in the database.

get_event_bookmarks()[source]
Return the list of Event handles in the bookmarks.

get_event_cursor()[source]
Return a reference to a cursor over Family objects. Example use:

with get_event_cursor() as cursor:
    for handle, event in cursor:
        # process event object pointed to by the handle
get_event_from_gramps_id(val)[source]
Find an Event in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Event exists, None is returned.

get_event_from_handle(handle)[source]
Return an Event in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Event exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Event is filtered out.

get_event_handles()[source]
Return a list of database handles, one handle for each Event in the database.

Warning For speed the keys are directly returned, so handles are bytes type
get_event_roles()[source]
Return a list of all custom event role names associated with Event instances in the database.

get_event_types()[source]
Return a list of all event types in the database.

get_family_attribute_types()[source]
Return a list of all Attribute types associated with Family instances in the database.

get_family_bookmarks()[source]
Return the list of Family handles in the bookmarks.

get_family_cursor()[source]
Return a reference to a cursor over Family objects. Example use:

with get_family_cursor() as cursor:
    for handle, family in cursor:
        # process family object pointed to by the handle
get_family_event_types()[source]
Deprecated: Use get_event_types

get_family_from_gramps_id(val)[source]
Find a Family in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Family exists, None is returned.

get_family_from_handle(handle)[source]
Return a Family in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Family exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Family is filtered out.

get_family_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Family in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by surnames.

locale (A GrampsLocale object.) – The locale to use for collation.

Warning For speed the keys are directly returned, so handles are bytes type
get_family_relation_types()[source]
Return a list of all relationship types associated with Family instances in the database.

get_feature(feature)[source]
Databases can implement certain features or not. The default is None, unless otherwise explicitly stated.

get_media_attribute_types()[source]
Return a list of all Attribute types associated with Media and MediaRef instances in the database.

get_media_bookmarks()[source]
Return the list of Media handles in the bookmarks.

get_media_cursor()[source]
Return a reference to a cursor over Media objects. Example use:

with get_media_cursor() as cursor:
    for handle, media in cursor:
        # process media object pointed to by the handle
get_media_from_gramps_id(val)[source]
Find a Media in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Media exists, None is returned.

get_media_from_handle(handle)[source]
Return a Media in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Object exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Media is filtered out.

get_media_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Media in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by title.

locale (A GrampsLocale object.) – The locale to use for collation.

Warning For speed the keys are directly returned, so handles are bytes type
get_mediapath()[source]
Return the default media path of the database.

get_name_group_keys()[source]
Return the defined names that have been assigned to a default grouping.

get_name_group_mapping(surname)[source]
Return the default grouping name for a surname.

get_name_types()[source]
Return a list of all custom names types associated with Person instances in the database.

get_note_bookmarks()[source]
Return the list of Note handles in the bookmarks.

get_note_cursor()[source]
Return a reference to a cursor over Note objects. Example use:

with get_note_cursor() as cursor:
    for handle, note in cursor:
        # process note object pointed to by the handle
get_note_from_gramps_id(val)[source]
Find a Note in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Note exists, None is returned.

get_note_from_handle(handle)[source]
Return a Note in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Note exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Note is filtered out.

get_note_handles()[source]
Return a list of database handles, one handle for each Note in the database.

Warning For speed the keys are directly returned, so handles are bytes type
get_note_types()[source]
Return a list of all custom note types associated with Note instances in the database.

get_number_of_citations()[source]
Return the number of citations currently in the database.

get_number_of_events()[source]
Return the number of events currently in the database.

get_number_of_families()[source]
Return the number of families currently in the database.

get_number_of_media()[source]
Return the number of media objects currently in the database.

get_number_of_notes()[source]
Return the number of notes currently in the database.

get_number_of_people()[source]
Return the number of people currently in the database.

get_number_of_places()[source]
Return the number of places currently in the database.

get_number_of_repositories()[source]
Return the number of source repositories currently in the database.

get_number_of_sources()[source]
Return the number of sources currently in the database.

get_number_of_tags()[source]
Return the number of tags currently in the database.

get_origin_types()[source]
Return a list of all custom origin types associated with Person/Surname instances in the database.

get_person_attribute_types()[source]
Return a list of all Attribute types associated with Person instances in the database.

get_person_cursor()[source]
Return a reference to a cursor over Person objects. Example use:

with get_person_cursor() as cursor:
    for handle, person in cursor:
        # process person object pointed to by the handle
get_person_event_types()[source]
Deprecated: Use get_event_types

get_person_from_gramps_id(val)[source]
Find a Person in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Person exists, None is returned.

get_person_from_handle(handle)[source]
Return a Person in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Person exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Person is filtered out.

get_person_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Person in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by surnames.

locale (A GrampsLocale object.) – The locale to use for collation.

Warning For speed the keys are directly returned, so handles are bytes type
get_place_bookmarks()[source]
Return the list of Place handles in the bookmarks.

get_place_cursor()[source]
Return a reference to a cursor over Place objects. Example use:

with get_place_cursor() as cursor:
    for handle, place in cursor:
        # process place object pointed to by the handle
get_place_from_gramps_id(val)[source]
Find a Place in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Place exists, None is returned.

get_place_from_handle(handle)[source]
Return a Place in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Place exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Place is filtered out.

get_place_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Place in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Place title.

locale (A GrampsLocale object.) – The locale to use for collation.

Warning For speed the keys are directly returned, so handles are bytes type
get_place_tree_cursor()[source]
Return a reference to a cursor that iterates over Place objects in the order they appear in the place hierarchy. Example use:

with get_place_tree_cursor() as cursor:
    for handle, place in cursor:
        # process place object pointed to by the handle
get_place_types()[source]
Return a list of all custom place types assocated with Place instances in the database.

get_raw_citation_data(handle)[source]
Return raw (serialized and pickled) Citation object from handle

get_raw_event_data(handle)[source]
Return raw (serialized and pickled) Event object from handle

get_raw_family_data(handle)[source]
Return raw (serialized and pickled) Family object from handle

get_raw_media_data(handle)[source]
Return raw (serialized and pickled) Family object from handle

get_raw_note_data(handle)[source]
Return raw (serialized and pickled) Note object from handle

get_raw_person_data(handle)[source]
Return raw (serialized and pickled) Person object from handle

get_raw_place_data(handle)[source]
Return raw (serialized and pickled) Place object from handle

get_raw_repository_data(handle)[source]
Return raw (serialized and pickled) Repository object from handle

get_raw_source_data(handle)[source]
Return raw (serialized and pickled) Source object from handle

get_raw_tag_data(handle)[source]
Return raw (serialized and pickled) Tag object from handle

get_repo_bookmarks()[source]
Return the list of Repository handles in the bookmarks.

get_repository_cursor()[source]
Return a reference to a cursor over Repository objects. Example use:

with get_repository_cursor() as cursor:
    for handle, repository in cursor:
        # process repository object pointed to by the handle
get_repository_from_gramps_id(val)[source]
Find a Repository in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Repository exists, None is returned.

get_repository_from_handle(handle)[source]
Return a Repository in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Repository exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Repository is filtered out.

get_repository_handles()[source]
Return a list of database handles, one handle for each Repository in the database.

Warning For speed the keys are directly returned, so handles are bytes type
get_repository_types()[source]
Return a list of all custom repository types associated with Repository instances in the database.

get_researcher()[source]
Return the Researcher instance, providing information about the owner of the database.

get_save_path()[source]
Return the save path of the file, or “” if one does not exist.

get_source_attribute_types()[source]
Return a list of all Attribute types associated with Source/Citation instances in the database.

get_source_bookmarks()[source]
Return the list of Source handles in the bookmarks.

get_source_cursor()[source]
Return a reference to a cursor over Source objects. Example use:

with get_source_cursor() as cursor:
    for handle, source in cursor:
        # process source object pointed to by the handle
get_source_from_gramps_id(val)[source]
Find a Source in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Source exists, None is returned.

get_source_from_handle(handle)[source]
Return a Source in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Source exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Source is filtered out.

get_source_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Source in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Source title.

locale (A GrampsLocale object.) – The locale to use for collation.

Warning For speed the keys are directly returned, so handles are bytes type
get_source_media_types()[source]
Return a list of all custom source media types associated with Source instances in the database.

get_summary()[source]
Returns dictionary of summary item. Should include, if possible:

_(“Number of people”) _(“Version”) _(“Data version”)

get_surname_list()[source]
Return the list of locale-sorted surnames contained in the database.

get_tag_cursor()[source]
Return a reference to a cursor over Tag objects. Example use:

with get_tag_cursor() as cursor:
    for handle, tag in cursor:
        # process tag object pointed to by the handle
get_tag_from_handle(handle)[source]
Return a Tag in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Tag exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Tag is filtered out.

get_tag_from_name(val)[source]
Find a Tag in the database from the passed Tag name.

If no such Tag exists, None is returned.

get_tag_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Tag in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Tag name.

locale (A GrampsLocale object.) – The locale to use for collation.

Warning For speed the keys are directly returned, so handles are bytes type
get_url_types()[source]
Return a list of all custom names types associated with Url instances in the database.

has_citation_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Citation table.

has_citation_handle(handle)[source]
Return True if the handle exists in the current Citation database.

has_event_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Event table.

has_event_handle(handle)[source]
Return True if the handle exists in the current Event database.

has_family_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Family table.

has_family_handle(handle)[source]
Return True if the handle exists in the current Family database.

has_media_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Media table.

has_media_handle(handle)[source]
Return True if the handle exists in the current Mediadatabase.

has_name_group_key(name)[source]
Return if a key exists in the name_group table.

has_note_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Note table.

has_note_handle(handle)[source]
Return True if the handle exists in the current Note database.

has_person_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Person table.

has_person_handle(handle)[source]
Return True if the handle exists in the current Person database.

has_place_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Place table.

has_place_handle(handle)[source]
Return True if the handle exists in the current Place database.

has_repository_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Repository table.

has_repository_handle(handle)[source]
Return True if the handle exists in the current Repository database.

has_source_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Source table.

has_source_handle(handle)[source]
Return True if the handle exists in the current Source database.

has_tag_handle(handle)[source]
Return True if the handle exists in the current Tag database.

is_open()[source]
Return True if the database has been opened.

iter_citation_handles()[source]
Return an iterator over handles for Citations in the database

iter_citations()[source]
Return an iterator over objects for Citations in the database

iter_event_handles()[source]
Return an iterator over handles for Events in the database

iter_events()[source]
Return an iterator over objects for Events in the database

iter_families()[source]
Return an iterator over objects for Families in the database

iter_family_handles()[source]
Return an iterator over handles for Families in the database

iter_media()[source]
Return an iterator over objects for Medias in the database

iter_media_handles()[source]
Return an iterator over handles for Media in the database

iter_note_handles()[source]
Return an iterator over handles for Notes in the database

iter_notes()[source]
Return an iterator over objects for Notes in the database

iter_people()[source]
Return an iterator over objects for Persons in the database

iter_person_handles()[source]
Return an iterator over handles for Persons in the database

iter_place_handles()[source]
Return an iterator over handles for Places in the database

iter_places()[source]
Return an iterator over objects for Places in the database

iter_repositories()[source]
Return an iterator over objects for Repositories in the database

iter_repository_handles()[source]
Return an iterator over handles for Repositories in the database

iter_source_handles()[source]
Return an iterator over handles for Sources in the database

iter_sources()[source]
Return an iterator over objects for Sources in the database

iter_tag_handles()[source]
Return an iterator over handles for Tags in the database

iter_tags()[source]
Return an iterator over objects for Tags in the database

load(name, callback, mode=None, force_schema_upgrade=False, force_bsddb_upgrade=False)[source]
Open the specified database.

method(fmt, *args)[source]
Convenience function to return database methods.

Parameters
fmt (str) – Method format string.

args (str) – Substitutions arguments.

Returns
Returns a database method or None.

Return type
method

Examples:

db.method('get_%s_from_handle, 'Person')
Returns the get_person_from_handle method.

db.method('get_%s_from_%s, 'Event', 'gramps_id')
Returns the get_event_from_gramps_id method.

db.method('get_%s_handles, 'Attribute')
Returns None.  Attribute is not a primary object.
Warning Formats ‘iter_%s’ and ‘get_number_of_%s’ are not yet implemented.
report_bm_change()[source]
Add 1 to the number of bookmark changes during this session.

request_rebuild()[source]
Notify clients that the data has changed significantly, and that all internal data dependent on the database should be rebuilt. Note that all rebuild signals on all objects are emitted at the same time. It is correct to assume that this is always the case.

Todo it might be better to replace these rebuild signals by one single database-rebuild signal.
requires_login()[source]
Returns True for backends that require a login dialog, else False.

set_citation_id_prefix(val)[source]
Set the naming template for Gramps Citation ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as C%d or C%04d.

set_event_id_prefix(val)[source]
Set the naming template for Gramps Event ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as E%d or E%04d.

set_family_id_prefix(val)[source]
Set the naming template for Gramps Family ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as F%d or F%04d.

set_feature(feature, value)[source]
Databases can implement certain features.

set_media_id_prefix(val)[source]
Set the naming template for Gramps Media ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as O%d or O%04d.

set_mediapath(path)[source]
Set the default media path for database.

set_note_id_prefix(val)[source]
Set the naming template for Gramps Note ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as N%d or N%04d.

set_person_id_prefix(val)[source]
Set the naming template for Gramps Person ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as I%d or I%04d.

set_place_id_prefix(val)[source]
Set the naming template for Gramps Place ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as P%d or P%04d.

set_prefixes(person, media, family, source, citation, place, event, repository, note)[source]
Set the prefixes for the gramps ids for all gramps objects

set_repository_id_prefix(val)[source]
Set the naming template for Gramps Repository ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as R%d or R%04d.

set_researcher(owner)[source]
Set the information about the owner of the database.

set_source_id_prefix(val)[source]
Set the naming template for Gramps Source ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as S%d or S%04d.

version_supported()[source]
Return True when the file has a supported version.

class gramps.gen.db.base.DbWriteBase[source]
Bases: gramps.gen.db.base.DbReadBase

Gramps database object. This object is a base class for all database interfaces. All methods raise NotImplementedError and must be implemented in the derived class as required.

add_child_to_family(family, child, mrel=<gramps.gen.lib.childreftype.ChildRefType object>, frel=<gramps.gen.lib.childreftype.ChildRefType object>, trans=None)[source]
Adds a child to a family.

add_citation(event, transaction, set_gid=True)[source]
Add an Citation to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_event(event, transaction, set_gid=True)[source]
Add an Event to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_family(family, transaction, set_gid=True)[source]
Add a Family to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_media(obj, transaction, set_gid=True)[source]
Add a Media to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_note(obj, transaction, set_gid=True)[source]
Add a Note to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_person(person, transaction, set_gid=True)[source]
Add a Person to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_place(place, transaction, set_gid=True)[source]
Add a Place to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_repository(obj, transaction, set_gid=True)[source]
Add a Repository to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_source(source, transaction, set_gid=True)[source]
Add a Source to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_tag(tag, transaction)[source]
Add a Tag to the database, assigning a handle if it has not already been defined.

add_to_surname_list(person, batch_transaction, name)[source]
Add surname from given person to list of surnames

commit_citation(event, transaction, change_time=None)[source]
Commit the specified Event to the database, storing the changes as part of the transaction.

commit_event(event, transaction, change_time=None)[source]
Commit the specified Event to the database, storing the changes as part of the transaction.

commit_family(family, transaction, change_time=None)[source]
Commit the specified Family to the database, storing the changes as part of the transaction.

commit_media(obj, transaction, change_time=None)[source]
Commit the specified Media to the database, storing the changes as part of the transaction.

commit_note(note, transaction, change_time=None)[source]
Commit the specified Note to the database, storing the changes as part of the transaction.

commit_person(person, transaction, change_time=None)[source]
Commit the specified Person to the database, storing the changes as part of the transaction.

commit_place(place, transaction, change_time=None)[source]
Commit the specified Place to the database, storing the changes as part of the transaction.

commit_repository(repository, transaction, change_time=None)[source]
Commit the specified Repository to the database, storing the changes as part of the transaction.

commit_source(source, transaction, change_time=None)[source]
Commit the specified Source to the database, storing the changes as part of the transaction.

commit_tag(tag, transaction, change_time=None)[source]
Commit the specified Tag to the database, storing the changes as part of the transaction.

delete_person_from_database(person, trans)[source]
Deletes a person from the database, cleaning up all associated references.

get_total()[source]
Get the total of primary objects.

get_undodb()[source]
Return the database that keeps track of Undo/Redo operations.

marriage_from_eventref_list(eventref_list)[source]
Get the marriage event from an eventref list.

rebuild_secondary(callback)[source]
Rebuild secondary indices

redo(update_history=True)[source]
Redo last transaction.

reindex_reference_map(callback)[source]
Reindex all primary records in the database.

remove_child_from_family(person_handle, family_handle, trans=None)[source]
Remove a person as a child of the family, deleting the family if it becomes empty.

remove_citation(handle, transaction)[source]
Remove the Event specified by the database handle from the database, preserving the change in the passed transaction.

remove_event(handle, transaction)[source]
Remove the Event specified by the database handle from the database, preserving the change in the passed transaction.

remove_family(handle, transaction)[source]
Remove the Family specified by the database handle from the database, preserving the change in the passed transaction.

remove_family_relationships(family_handle, trans=None)[source]
Remove a family and its relationships.

remove_from_surname_list(person)[source]
Check whether there are persons with the same surname left in the database.

If not then we need to remove the name from the list. The function must be overridden in the derived class.

remove_media(handle, transaction)[source]
Remove the MediaPerson specified by the database handle from the database, preserving the change in the passed transaction.

remove_note(handle, transaction)[source]
Remove the Note specified by the database handle from the database, preserving the change in the passed transaction.

remove_parent_from_family(person_handle, family_handle, trans=None)[source]
Remove a person as either the father or mother of a family, deleting the family if it becomes empty.

remove_person(handle, transaction)[source]
Remove the Person specified by the database handle from the database, preserving the change in the passed transaction.

remove_place(handle, transaction)[source]
Remove the Place specified by the database handle from the database, preserving the change in the passed transaction.

remove_repository(handle, transaction)[source]
Remove the Repository specified by the database handle from the database, preserving the change in the passed transaction.

remove_source(handle, transaction)[source]
Remove the Source specified by the database handle from the database, preserving the change in the passed transaction.

remove_tag(handle, transaction)[source]
Remove the Tag specified by the database handle from the database, preserving the change in the passed transaction.

set_birth_death_index(person)[source]
Set the birth and death indices for a person.

set_default_person_handle(handle)[source]
Set the default Person to the passed instance.

set_name_group_mapping(name, group)[source]
Set the default grouping name for a surname.

Needs to be overridden in the derived class.

transaction_abort(transaction)[source]
Revert the changes made to the database so far during the transaction.

transaction_begin(transaction)[source]
Prepare the database for the start of a new transaction.

Two modes should be provided: transaction.batch=False for ordinary database operations that will be encapsulated in database transactions to make them ACID and that are added to Gramps transactions so that they can be undone. And transaction.batch=True for lengthy database operations, that benefit from a speedup by making them none ACID, and that can’t be undone. The user is warned and is asked for permission before the start of such database operations.

Parameters
transaction (DbTxn) – Gramps transaction …

Returns
Returns the Gramps transaction.

Return type
DbTxn

transaction_commit(transaction)[source]
Make the changes to the database final and add the content of the transaction to the undo database.

undo(update_history=True)[source]
Undo last transaction.

GrampsDbTxn
Exports the DbTxn class for managing Gramps transactions and the undo database.

class gramps.gen.db.txn.DbTxn(msg, grampsdb, batch=False, **kwargs)[source]
Bases: collections.defaultdict

Define a group of database commits that define a single logical operation.

add(obj_type, trans_type, handle, old_data, new_data)[source]
Add a commit operation to the Transaction.

The obj_type is a constant that indicates what type of PrimaryObject is being added. The handle is the object’s database handle, and the data is the tuple returned by the object’s serialize method.

batch
commitdb
db
first
get_description()[source]
Return the text string that describes the logical operation performed by the Transaction.

get_recnos(reverse=False)[source]
Return a list of record numbers associated with the transaction.

While the list is an arbitrary index of integers, it can be used to indicate record numbers for a database.

get_record(recno)[source]
Return a tuple representing the PrimaryObject type, database handle for the PrimaryObject, and a tuple representing the data created by the object’s serialize method.

last
msg
set_description(msg)[source]
Set the text string that describes the logical operation performed by the Transaction.

timestamp
DbConst
Declare constants used by database modules

GrampsDbException
Exceptions generated by the Db package.

exception gramps.gen.db.exceptions.BsddbDowngradeError(env_version, bdb_version)[source]
Bases: Exception

Error used to report that the Berkeley database used to create the family tree is of a version that is too new to be supported by the current version.

exception gramps.gen.db.exceptions.BsddbDowngradeRequiredError(env_version, bdb_version)[source]
Bases: Exception

Error used to report that the Berkeley database used to create the family tree is of a version that is newer than the current version, but it may be possible to open the tree, because the difference is only a point upgrade (i.e. a difference in the last digit of the version tuple).

exception gramps.gen.db.exceptions.BsddbUpgradeRequiredError(env_version, bsddb_version)[source]
Bases: Exception

Error used to report that the Berkeley database used to create the family tree is of a version that is too new to be supported by the current version.

exception gramps.gen.db.exceptions.DbConnectionError(msg, settings_file)[source]
Bases: Exception

Error used to report that a database connection failed.

exception gramps.gen.db.exceptions.DbEnvironmentError(msg)[source]
Bases: Exception

Error used to report that the database ‘environment’ could not be opened. Most likely, the database was created by a different version of the underlying database engine.

exception gramps.gen.db.exceptions.DbException(value)[source]
Bases: Exception

exception gramps.gen.db.exceptions.DbPythonError(tree_vers, min_vers, max_vers)[source]
Bases: Exception

Error used to report that a file could not be read because it is written in an unsupported version of the Python format.

exception gramps.gen.db.exceptions.DbTransactionCancel(value)[source]
Bases: Exception

Error used to indicate that a transaction needs to be canceled, for example becuase it is lengthy and the users requests so.

exception gramps.gen.db.exceptions.DbUpgradeRequiredError(oldschema, newschema)[source]
Bases: Exception

Error used to report that a database needs to be upgraded before it can be used.

exception gramps.gen.db.exceptions.DbVersionError(tree_vers, min_vers, max_vers)[source]
Bases: Exception

Error used to report that a file could not be read because it is written in an unsupported version of the file format.

exception gramps.gen.db.exceptions.DbWriteFailure(value, value2='')[source]
Bases: Exception

Error used to indicate that a write to a database has failed.

messages()[source]
exception gramps.gen.db.exceptions.PythonDowngradeError(db_python_version, current_python_version)[source]
Bases: Exception

Error used to report that the Python version used to create the family tree (i.e. Python3) is a version that is newer than the current version (i.e. Python2), so the Family Tree cannot be opened

exception gramps.gen.db.exceptions.PythonUpgradeRequiredError(db_python_version, current_python_version)[source]
Bases: Exception

Error used to report that the Python version used to create the family tree (i.e. Python2) is earlier than the current Python version (i.e. Python3), so the Family Tree needs to be upgraded.

GrampsDbUndo
class gramps.gen.db.undoredo.DbUndo(db)[source]
Bases: object

Base class for the Gramps undo/redo manager. Needs to be subclassed for use with a real backend.

append(value)[source]
Add a new entry on the end. Needs to be overridden in the derived class.

clear()[source]
Clear the undo/redo list (but not the backing storage)

close()[source]
Close the backing storage. Needs to be overridden in the derived class.

commit(txn, msg)[source]
Commit the transaction to the undo/redo database. “txn” should be an instance of Gramps transaction class

db
open(value)[source]
Open the backing storage. Needs to be overridden in the derived class.

redo(update_history=True)[source]
Redo a previously committed, then undone, transaction

redo_count
redoq
undo(update_history=True)[source]
Undo a previously committed transaction

undo_count
undo_history_timestamp
undodb
undoq
Generic
class gramps.gen.db.generic.Cursor(iterator)[source]
Bases: object

close()[source]
first()[source]
iter()[source]
next()[source]
class gramps.gen.db.generic.DbGeneric(directory=None)[source]
Bases: gramps.gen.db.base.DbWriteBase, gramps.gen.db.base.DbReadBase, gramps.gen.updatecallback.UpdateCallback, gramps.gen.utils.callback.Callback

A Gramps Database Backend. This replicates the grampsdb functions.

VERSION = (18, 0, 0)
add_citation(citation, trans, set_gid=True)[source]
Add an Citation to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_event(event, trans, set_gid=True)[source]
Add an Event to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_family(family, trans, set_gid=True)[source]
Add a Family to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_media(media, trans, set_gid=True)[source]
Add a Media to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_note(note, trans, set_gid=True)[source]
Add a Note to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_person(person, trans, set_gid=True)[source]
Add a Person to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_place(place, trans, set_gid=True)[source]
Add a Place to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_repository(repository, trans, set_gid=True)[source]
Add a Repository to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_source(source, trans, set_gid=True)[source]
Add a Source to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_tag(tag, trans)[source]
Add a Tag to the database, assigning a handle if it has not already been defined.

add_to_surname_list(person, batch_transaction)[source]
Add surname to surname list

close(update=True, user=None)[source]
Close the database. if update is False, don’t change access times, etc.

commit_citation(citation, trans, change_time=None)[source]
Commit the specified Citation to the database, storing the changes as part of the transaction.

commit_event(event, trans, change_time=None)[source]
Commit the specified Event to the database, storing the changes as part of the transaction.

commit_family(family, trans, change_time=None)[source]
Commit the specified Family to the database, storing the changes as part of the transaction.

commit_media(media, trans, change_time=None)[source]
Commit the specified Media to the database, storing the changes as part of the transaction.

commit_note(note, trans, change_time=None)[source]
Commit the specified Note to the database, storing the changes as part of the transaction.

commit_person(person, trans, change_time=None)[source]
Commit the specified Person to the database, storing the changes as part of the transaction.

commit_place(place, trans, change_time=None)[source]
Commit the specified Place to the database, storing the changes as part of the transaction.

commit_repository(repository, trans, change_time=None)[source]
Commit the specified Repository to the database, storing the changes as part of the transaction.

commit_source(source, trans, change_time=None)[source]
Commit the specified Source to the database, storing the changes as part of the transaction.

commit_tag(tag, trans, change_time=None)[source]
Commit the specified Tag to the database, storing the changes as part of the transaction.

db_has_bm_changes()[source]
Return whethere there were bookmark changes during the session.

find_next_citation_gramps_id()[source]
Return the next available GRAMPS’ ID for a Citation object based off the citation ID prefix.

find_next_event_gramps_id()[source]
Return the next available GRAMPS’ ID for a Event object based off the event ID prefix.

find_next_family_gramps_id()[source]
Return the next available GRAMPS’ ID for a Family object based off the family ID prefix.

find_next_media_gramps_id()[source]
Return the next available GRAMPS’ ID for a Media object based off the media object ID prefix.

find_next_note_gramps_id()[source]
Return the next available GRAMPS’ ID for a Note object based off the note ID prefix.

find_next_person_gramps_id()[source]
Return the next available GRAMPS’ ID for a Person object based off the person ID prefix.

find_next_place_gramps_id()[source]
Return the next available GRAMPS’ ID for a Place object based off the place ID prefix.

find_next_repository_gramps_id()[source]
Return the next available GRAMPS’ ID for a Respository object based off the repository ID prefix.

find_next_source_gramps_id()[source]
Return the next available GRAMPS’ ID for a Source object based off the source ID prefix.

get_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_child_reference_types()[source]
Return a list of all child reference types assocated with Family instances in the database.

get_citation_bookmarks()[source]
Return the list of Citation handles in the bookmarks.

get_citation_cursor()[source]
Return a reference to a cursor over Citation objects. Example use:

with get_citation_cursor() as cursor:
for handle, citation in cursor:
# process citation object pointed to by the handle

get_citation_from_gramps_id(gramps_id)[source]
Find a Citation in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Citation exists, None is returned.

get_citation_from_handle(handle)[source]
Return a Citation in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Citation exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Citation is filtered out.

get_citation_gramps_ids()[source]
Return a list of Gramps IDs, one ID for each Citation in the database.

get_dbid()[source]
We use the file directory name as the unique ID for this database on this computer.

get_dbname()[source]
In DbGeneric, the database is in a text file at the path

get_default_handle()[source]
Return the default Person of the database.

get_default_person()[source]
Return the default Person of the database.

get_event_attribute_types()[source]
Return a list of all Attribute types assocated with Event instances in the database.

get_event_bookmarks()[source]
Return the list of Event handles in the bookmarks.

get_event_cursor()[source]
Return a reference to a cursor over Family objects. Example use:

with get_event_cursor() as cursor:
for handle, event in cursor:
# process event object pointed to by the handle

get_event_from_gramps_id(gramps_id)[source]
Find an Event in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Event exists, None is returned.

get_event_from_handle(handle)[source]
Return an Event in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Event exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Event is filtered out.

get_event_gramps_ids()[source]
Return a list of Gramps IDs, one ID for each Event in the database.

get_event_roles()[source]
Return a list of all custom event role names assocated with Event instances in the database.

get_event_types()[source]
Return a list of all event types in the database.

get_family_attribute_types()[source]
Return a list of all Attribute types assocated with Family instances in the database.

get_family_bookmarks()[source]
Return the list of Family handles in the bookmarks.

get_family_cursor()[source]
Return a reference to a cursor over Family objects. Example use:

with get_family_cursor() as cursor:
for handle, family in cursor:
# process family object pointed to by the handle

get_family_event_types()[source]
Deprecated: Use get_event_types

get_family_from_gramps_id(gramps_id)[source]
Find a Family in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Family exists, None is returned.

get_family_from_handle(handle)[source]
Return a Family in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Family exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Family is filtered out.

get_family_gramps_ids()[source]
Return a list of Gramps IDs, one ID for each Family in the database.

get_family_relation_types()[source]
Return a list of all relationship types assocated with Family instances in the database.

get_gender_stats()[source]
Returns a dictionary of {given_name: (male_count, female_count, unknown_count)}

get_media_attribute_types()[source]
Return a list of all Attribute types assocated with Media and MediaRef instances in the database.

get_media_bookmarks()[source]
Return the list of Media handles in the bookmarks.

get_media_cursor()[source]
Return a reference to a cursor over Media objects. Example use:

with get_media_cursor() as cursor:
for handle, media in cursor:
# process media object pointed to by the handle

get_media_from_gramps_id(gramps_id)[source]
Find a Media in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Media exists, None is returned.

get_media_from_handle(handle)[source]
Return a Media in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Object exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Media is filtered out.

get_media_gramps_ids()[source]
Return a list of Gramps IDs, one ID for each Media in the database.

get_mediapath()[source]
Return the default media path of the database.

get_name_types()[source]
Return a list of all custom names types assocated with Person instances in the database.

get_note_bookmarks()[source]
Return the list of Note handles in the bookmarks.

get_note_cursor()[source]
Return a reference to a cursor over Note objects. Example use:

with get_note_cursor() as cursor:
for handle, note in cursor:
# process note object pointed to by the handle

get_note_from_gramps_id(gramps_id)[source]
Find a Note in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Note exists, None is returned.

get_note_from_handle(handle)[source]
Return a Note in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Note exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Note is filtered out.

get_note_gramps_ids()[source]
Return a list of Gramps IDs, one ID for each Note in the database.

get_note_types()[source]
Return a list of all custom note types assocated with Note instances in the database.

get_number_of_citations()[source]
Return the number of citations currently in the database.

get_number_of_events()[source]
Return the number of events currently in the database.

get_number_of_families()[source]
Return the number of families currently in the database.

get_number_of_media()[source]
Return the number of media objects currently in the database.

get_number_of_notes()[source]
Return the number of notes currently in the database.

get_number_of_people()[source]
Return the number of people currently in the database.

get_number_of_places()[source]
Return the number of places currently in the database.

get_number_of_repositories()[source]
Return the number of source repositories currently in the database.

get_number_of_sources()[source]
Return the number of sources currently in the database.

get_number_of_tags()[source]
Return the number of tags currently in the database.

get_origin_types()[source]
Return a list of all custom origin types assocated with Person/Surname instances in the database.

get_person_attribute_types()[source]
Return a list of all Attribute types assocated with Person instances in the database.

get_person_cursor()[source]
Return a reference to a cursor over Person objects. Example use:

with get_person_cursor() as cursor:
for handle, person in cursor:
# process person object pointed to by the handle

get_person_event_types()[source]
Deprecated: Use get_event_types

get_person_from_gramps_id(gramps_id)[source]
Find a Person in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Person exists, None is returned.

get_person_from_handle(handle)[source]
Return a Person in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Person exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Person is filtered out.

get_person_gramps_ids()[source]
Return a list of Gramps IDs, one ID for each Person in the database.

get_place_bookmarks()[source]
Return the list of Place handles in the bookmarks.

get_place_cursor()[source]
Return a reference to a cursor over Place objects. Example use:

with get_place_cursor() as cursor:
for handle, place in cursor:
# process place object pointed to by the handle

get_place_from_gramps_id(gramps_id)[source]
Find a Place in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Place exists, None is returned.

get_place_from_handle(handle)[source]
Return a Place in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Place exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Place is filtered out.

get_place_gramps_ids()[source]
Return a list of Gramps IDs, one ID for each Place in the database.

get_place_tree_cursor()[source]
Return a reference to a cursor that iterates over Place objects in the order they appear in the place hierarchy. Example use:

with get_place_tree_cursor() as cursor:
    for handle, place in cursor:
        # process place object pointed to by the handle
get_place_types()[source]
Return a list of all custom place types assocated with Place instances in the database.

get_raw_citation_data(handle)[source]
Return raw (serialized and pickled) Citation object from handle

get_raw_event_data(handle)[source]
Return raw (serialized and pickled) Event object from handle

get_raw_family_data(handle)[source]
Return raw (serialized and pickled) Family object from handle

get_raw_media_data(handle)[source]
Return raw (serialized and pickled) Family object from handle

get_raw_note_data(handle)[source]
Return raw (serialized and pickled) Note object from handle

get_raw_person_data(handle)[source]
Return raw (serialized and pickled) Person object from handle

get_raw_place_data(handle)[source]
Return raw (serialized and pickled) Place object from handle

get_raw_repository_data(handle)[source]
Return raw (serialized and pickled) Repository object from handle

get_raw_source_data(handle)[source]
Return raw (serialized and pickled) Source object from handle

get_raw_tag_data(handle)[source]
Return raw (serialized and pickled) Tag object from handle

get_repo_bookmarks()[source]
Return the list of Repository handles in the bookmarks.

get_repository_cursor()[source]
Return a reference to a cursor over Repository objects. Example use:

with get_repository_cursor() as cursor:
for handle, repository in cursor:
# process repository object pointed to by the handle

get_repository_from_gramps_id(gramps_id)[source]
Find a Repository in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Repository exists, None is returned.

get_repository_from_handle(handle)[source]
Return a Repository in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Repository exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Repository is filtered out.

get_repository_gramps_ids()[source]
Return a list of Gramps IDs, one ID for each Repository in the database.

get_repository_types()[source]
Return a list of all custom repository types assocated with Repository instances in the database.

get_researcher()[source]
Return the Researcher instance, providing information about the owner of the database.

get_save_path()[source]
Return the save path of the file, or “” if one does not exist.

get_source_attribute_types()[source]
Return a list of all Attribute types assocated with Source/Citation instances in the database.

get_source_bookmarks()[source]
Return the list of Source handles in the bookmarks.

get_source_cursor()[source]
Return a reference to a cursor over Source objects. Example use:

with get_source_cursor() as cursor:
for handle, source in cursor:
# process source object pointed to by the handle

get_source_from_gramps_id(gramps_id)[source]
Find a Source in the database from the passed Gramps ID.

Parameters
val (str or bytes) – gramps_id of the object to search for.

If no such Source exists, None is returned.

get_source_from_handle(handle)[source]
Return a Source in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Source exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Source is filtered out.

get_source_gramps_ids()[source]
Return a list of Gramps IDs, one ID for each Source in the database.

get_source_media_types()[source]
Return a list of all custom source media types assocated with Source instances in the database.

get_summary()[source]
Returns dictionary of summary item. Should include, if possible:

_(“Number of people”) _(“Version”) _(“Data version”)

get_surname_list()[source]
Return the list of locale-sorted surnames contained in the database.

get_tag_cursor()[source]
Return a reference to a cursor over Tag objects. Example use:

with get_tag_cursor() as cursor:
for handle, tag in cursor:
# process tag object pointed to by the handle

get_tag_from_handle(handle)[source]
Return a Tag in the database from the passed handle.

Parameters
handle (str or bytes) – handle of the object to search for.

If no such Tag exists, a HandleError is raised. Note: if used through a proxy (Filter for reports etc.) a ‘None’ is returned in cases where the Tag is filtered out.

get_undodb()[source]
Return the database that keeps track of Undo/Redo operations.

get_url_types()[source]
Return a list of all custom names types assocated with Url instances in the database.

has_citation_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Citation table.

has_citation_handle(handle)[source]
Return True if the handle exists in the current Citation database.

has_event_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Event table.

has_event_handle(handle)[source]
Return True if the handle exists in the current Event database.

has_family_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Family table.

has_family_handle(handle)[source]
Return True if the handle exists in the current Family database.

has_media_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Media table.

has_media_handle(handle)[source]
Return True if the handle exists in the current Mediadatabase.

has_note_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Note table.

has_note_handle(handle)[source]
Return True if the handle exists in the current Note database.

has_person_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Person table.

has_person_handle(handle)[source]
Return True if the handle exists in the current Person database.

has_place_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Place table.

has_place_handle(handle)[source]
Return True if the handle exists in the current Place database.

has_repository_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Repository table.

has_repository_handle(handle)[source]
Return True if the handle exists in the current Repository database.

has_source_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Source table.

has_source_handle(handle)[source]
Return True if the handle exists in the current Source database.

has_tag_handle(handle)[source]
Return True if the handle exists in the current Tag database.

is_open()[source]
Return True if the database has been opened.

iter_citation_handles()[source]
Return an iterator over database handles, one handle for each Citation in the database.

iter_citations()[source]
Return an iterator over objects for Citations in the database

iter_event_handles()[source]
Return an iterator over handles for Events in the database

iter_events()[source]
Return an iterator over objects for Events in the database

iter_families()[source]
Return an iterator over objects for Families in the database

iter_family_handles()[source]
Return an iterator over handles for Families in the database

iter_media()[source]
Return an iterator over objects for Medias in the database

iter_media_handles()[source]
Return an iterator over handles for Media in the database

iter_note_handles()[source]
Return an iterator over handles for Notes in the database

iter_notes()[source]
Return an iterator over objects for Notes in the database

iter_people()[source]
Return an iterator over objects for Persons in the database

iter_person_handles()[source]
Return an iterator over handles for Persons in the database

iter_place_handles()[source]
Return an iterator over handles for Places in the database

iter_places()[source]
Return an iterator over objects for Places in the database

iter_repositories()[source]
Return an iterator over objects for Repositories in the database

iter_repository_handles()[source]
Return an iterator over handles for Repositories in the database

iter_source_handles()[source]
Return an iterator over handles for Sources in the database

iter_sources()[source]
Return an iterator over objects for Sources in the database

iter_tag_handles()[source]
Return an iterator over handles for Tags in the database

iter_tags()[source]
Return an iterator over objects for Tags in the database

load(directory, callback=None, mode='w', force_schema_upgrade=False, force_bsddb_upgrade=False, force_bsddb_downgrade=False, force_python_upgrade=False, update=True, username=None, password=None)[source]
If update is False: then don’t update any files

redo(update_history=True)[source]
Redo last transaction.

remove_citation(handle, transaction)[source]
Remove the Citation specified by the database handle from the database, preserving the change in the passed transaction.

remove_event(handle, transaction)[source]
Remove the Event specified by the database handle from the database, preserving the change in the passed transaction.

remove_family(handle, transaction)[source]
Remove the Family specified by the database handle from the database, preserving the change in the passed transaction.

remove_from_surname_list(person)[source]
Check whether there are persons with the same surname left in the database.

If not then we need to remove the name from the list. The function must be overridden in the derived class.

remove_media(handle, transaction)[source]
Remove the MediaPerson specified by the database handle from the database, preserving the change in the passed transaction.

remove_note(handle, transaction)[source]
Remove the Note specified by the database handle from the database, preserving the change in the passed transaction.

remove_person(handle, transaction)[source]
Remove the Person specified by the database handle from the database, preserving the change in the passed transaction.

remove_place(handle, transaction)[source]
Remove the Place specified by the database handle from the database, preserving the change in the passed transaction.

remove_repository(handle, transaction)[source]
Remove the Repository specified by the database handle from the database, preserving the change in the passed transaction.

remove_source(handle, transaction)[source]
Remove the Source specified by the database handle from the database, preserving the change in the passed transaction.

remove_tag(handle, transaction)[source]
Remove the Tag specified by the database handle from the database, preserving the change in the passed transaction.

report_bm_change()[source]
Add 1 to the number of bookmark changes during this session.

request_rebuild()[source]
Notify clients that the data has changed significantly, and that all internal data dependent on the database should be rebuilt. Note that all rebuild signals on all objects are emitted at the same time. It is correct to assume that this is always the case.

Todo it might be better to replace these rebuild signals by one single database-rebuild signal.
save_gender_stats(gstats)[source]
set_citation_id_prefix(val)[source]
Set the naming template for Gramps Citation ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as C%d or C%04d.

set_default_person_handle(handle)[source]
Set the default Person to the passed instance.

set_event_id_prefix(val)[source]
Set the naming template for Gramps Event ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as E%d or E%04d.

set_family_id_prefix(val)[source]
Set the naming template for Gramps Family ID values. The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as F%d or F%04d.

set_media_id_prefix(val)[source]
Set the naming template for Gramps Media ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as O%d or O%04d.

set_mediapath(mediapath)[source]
Set the default media path for database.

set_note_id_prefix(val)[source]
Set the naming template for Gramps Note ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as N%d or N%04d.

set_person_id_prefix(val)[source]
Set the naming template for Gramps Person ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as I%d or I%04d.

set_place_id_prefix(val)[source]
Set the naming template for Gramps Place ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as P%d or P%04d.

set_prefixes(person, media, family, source, citation, place, event, repository, note)[source]
Set the prefixes for the gramps ids for all gramps objects

set_repository_id_prefix(val)[source]
Set the naming template for Gramps Repository ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as R%d or R%04d.

set_researcher(owner)[source]
Set the information about the owner of the database.

set_source_id_prefix(val)[source]
Set the naming template for Gramps Source ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as S%d or S%04d.

transaction_begin(transaction)[source]
Transactions are handled automatically by the db layer.

undo(update_history=True)[source]
Undo last transaction.

version_supported()[source]
Return True when the file has a supported version.

class gramps.gen.db.generic.DbGenericUndo(grampsdb, path)[source]
Bases: gramps.gen.db.undoredo.DbUndo

append(value)[source]
Add a new entry on the end. Needs to be overridden in the derived class.

close()[source]
Close the backing storage. Needs to be overridden in the derived class.

open(value=None)[source]
Open the backing storage. Needs to be overridden in the derived class.

undo_sigs(sigs, undo)[source]
Helper method to undo/redo the signals for changes made We want to do deletes and adds first Note that if ‘undo’ we swap emits

gramps.gen.db.generic.touch(fname, mode=438, dir_fd=None, **kwargs)[source]
DummyDb
Dummy database. This database is always empty and is read only.

It is provided for the initial database on loading Gramps, and also as a database when a normal database is closed.

Most of the code in Gramps uses dbstate.db.is_open() to determine whether data can be fetched from a database (essentially to determine whether there is a database to fetch data from). Thus, dbstate.db cannot be left as ‘None’ because None has no ‘is_open’ attribute. Therefore this database class is provided so that it can be instantiated for dbstate.db.

FIXME: Ideally, only is_open() needs to be implemented here, bacause that is the only method that should really be called, but the Gramps code is not perfect, and many other methods are called. Calls of other methods could be considered bugs, so when these are fixed, this class could be reduced.

FIXME: Errors in calling these methods (e.g. accessing data when the database is closed) should result in exceptions. However, at present (mid-2016) there are so many cases where these methods are called in error that raising exceptions would be too disruptive. Hence such errors only result in a warning log message and a ‘meaningful’ result is returned. When the rest of Gramps code is fixed, these methods should be changed to generate exceptions. Possibly by globally changing ‘LOG.debug’ to ‘raise DbException’.

class gramps.gen.db.dummydb.Bookmarks(default=[])[source]
Bases: object

Dummy Bookmarks class. This needs to be defined here, because get is used to return the bookmark.

append(item)[source]
Append a bookmark to the list

append_list(blist)[source]
Append a list of bookmarks to the bookmark

close()[source]
Close the bookmark, deleting the data.

get()[source]
Get the current bookmark list

insert(pos, item)[source]
Insert an item at a specified place in thebookmark list

pop(item)[source]
Pop an item off the bookmark list, returning the popped item

remove(item)[source]
Remove an item from the bookmark

set(new_list)[source]
Set the bookmark to a new list

class gramps.gen.db.dummydb.DummyDb[source]
Bases: gramps.gen.db.dummydb.NewBaseClass

Gramps database object. This object is a dummy database class that is always empty and is read-only.

close(update=True, user=None)[source]
Close the specified database.

db_has_bm_changes()[source]
Return whether there were bookmark changes during the session.

find_backlink_handles(handle, include_classes=None)[source]
Find all objects that hold a reference to the object handle.

Returns an iterator over a list of (class_name, handle) tuples.

Parameters
handle (database handle) – handle of the object to search for.

include_classes (list of class names) – list of class names to include in the results. Default is None which includes all classes.

This default implementation does a sequential scan through all the primary object databases and is very slow. Backends can override this method to provide much faster implementations that make use of additional capabilities of the backend.

Note that this is a generator function, it returns a iterator for use in loops. If you want a list of the results use:

result_list = list(find_backlink_handles(handle))
find_initial_person()[source]
Returns first person in the database

find_next_event_gramps_id()[source]
Return the next available Gramps ID for a Event object based off the event ID prefix.

find_next_family_gramps_id()[source]
Return the next available Gramps ID for a Family object based off the family ID prefix.

find_next_media_gramps_id()[source]
Return the next available Gramps ID for a Media object based off the media object ID prefix.

find_next_note_gramps_id()[source]
Return the next available Gramps ID for a Note object based off the note ID prefix.

find_next_person_gramps_id()[source]
Return the next available Gramps ID for a Person object based off the person ID prefix.

find_next_place_gramps_id()[source]
Return the next available Gramps ID for a Place object based off the place ID prefix.

find_next_repository_gramps_id()[source]
Return the next available Gramps ID for a Repository object based off the repository ID prefix.

find_next_source_gramps_id()[source]
Return the next available Gramps ID for a Source object based off the source ID prefix.

get_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_child_reference_types()[source]
Return a list of all child reference types associated with Family instances in the database.

get_citation_bookmarks()[source]
Return the list of Citation handles in the bookmarks.

get_citation_cursor()[source]
Return a reference to a cursor over Citation objects

get_citation_from_gramps_id(val)[source]
Find a Citation in the database from the passed Gramps ID.

If no such Citation exists, None is returned.

get_citation_from_handle(handle)[source]
Find a Citation in the database from the passed Gramps ID.

If no such Citation exists, a HandleError is raised.

get_citation_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Citation in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Citation title.

locale (A GrampsLocale object.) – The locale to use for collation.

get_dbid()[source]
A unique ID for this database on this computer.

get_dbname()[source]
A name for this database on this computer.

get_default_handle()[source]
Return the default Person of the database.

get_default_person()[source]
Return the default Person of the database.

get_event_attribute_types()[source]
Return a list of all Attribute types assocated with Event instances in the database.

get_event_bookmarks()[source]
Return the list of Event handles in the bookmarks.

get_event_cursor()[source]
Return a reference to a cursor over event objects

get_event_from_gramps_id(val)[source]
Find an Event in the database from the passed Gramps ID.

If no such Event exists, None is returned.

get_event_from_handle(handle)[source]
Find a Event in the database from the passed Gramps ID.

If no such Event exists, a HandleError is raised.

get_event_handles()[source]
Return a list of database handles, one handle for each Event in the database.

get_event_roles()[source]
Return a list of all custom event role names associated with Event instances in the database.

get_event_types()[source]
Return a list of all event types in the database.

get_family_attribute_types()[source]
Return a list of all Attribute types associated with Family instances in the database.

get_family_bookmarks()[source]
Return the list of Family handles in the bookmarks.

get_family_cursor()[source]
Return a reference to a cursor over Family objects

get_family_event_types()[source]
Deprecated: Use get_event_types

get_family_from_gramps_id(val)[source]
Find a Family in the database from the passed Gramps ID.

If no such Family exists, None is returned. Need to be overridden by the derived class.

get_family_from_handle(handle)[source]
Find a Family in the database from the passed Gramps ID.

If no such Family exists, a HandleError is raised.

get_family_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Family in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by surnames.

locale (A GrampsLocale object.) – The locale to use for collation.

get_family_relation_types()[source]
Return a list of all relationship types associated with Family instances in the database.

get_feature(feature)[source]
Databases can implement certain features or not. The default is None, unless otherwise explicitly stated.

get_media_attribute_types()[source]
Return a list of all Attribute types associated with Media and MediaRef instances in the database.

get_media_bookmarks()[source]
Return the list of Media handles in the bookmarks.

get_media_cursor()[source]
Return a reference to a cursor over Media objects

get_media_from_gramps_id(val)[source]
Find a Media in the database from the passed Gramps ID.

If no such Media exists, None is returned.

get_media_from_handle(handle)[source]
Find an Object in the database from the passed Gramps ID.

If no such Object exists, a HandleError is raised.

get_media_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Media in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by title.

locale (A GrampsLocale object.) – The locale to use for collation.

get_mediapath()[source]
Return the default media path of the database.

get_name_group_keys()[source]
Return the defined names that have been assigned to a default grouping.

get_name_group_mapping(surname)[source]
Return the default grouping name for a surname.

get_name_types()[source]
Return a list of all custom names types associated with Person instances in the database.

get_note_bookmarks()[source]
Return the list of Note handles in the bookmarks.

get_note_cursor()[source]
Return a reference to a cursor over Note objects

get_note_from_gramps_id(val)[source]
Find a Note in the database from the passed Gramps ID.

If no such Note exists, None is returned.

get_note_from_handle(handle)[source]
Find a Note in the database from the passed Gramps ID.

If no such Note exists, a HandleError is raised.

get_note_handles()[source]
Return a list of database handles, one handle for each Note in the database.

get_note_types()[source]
Return a list of all custom note types associated with Note instances in the database.

get_number_of_events()[source]
Return the number of events currently in the database.

get_number_of_families()[source]
Return the number of families currently in the database.

get_number_of_media()[source]
Return the number of media objects currently in the database.

get_number_of_notes()[source]
Return the number of notes currently in the database.

get_number_of_people()[source]
Return the number of people currently in the database.

get_number_of_places()[source]
Return the number of places currently in the database.

get_number_of_repositories()[source]
Return the number of source repositories currently in the database.

get_number_of_sources()[source]
Return the number of sources currently in the database.

get_number_of_tags()[source]
Return the number of tags currently in the database.

get_origin_types()[source]
Return a list of all custom origin types associated with Person/Surname instances in the database.

get_person_attribute_types()[source]
Return a list of all Attribute types associated with Person instances in the database.

get_person_cursor()[source]
Return a reference to a cursor over Person objects

get_person_event_types()[source]
Deprecated: Use get_event_types

get_person_from_gramps_id(val)[source]
Find a Person in the database from the passed Gramps ID.

If no such Person exists, None is returned.

get_person_from_handle(handle)[source]
Find a Person in the database from the passed Gramps ID.

If no such Person exists, a HandleError is raised.

get_person_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Person in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by surnames.

locale (A GrampsLocale object.) – The locale to use for collation.

get_place_bookmarks()[source]
Return the list of Place handles in the bookmarks.

get_place_cursor()[source]
Return a reference to a cursor over Place objects

get_place_from_gramps_id(val)[source]
Find a Place in the database from the passed Gramps ID.

If no such Place exists, None is returned.

get_place_from_handle(handle)[source]
Find a Place in the database from the passed Gramps ID.

If no such Place exists, a HandleError is raised.

get_place_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Place in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Place title.

locale (A GrampsLocale object.) – The locale to use for collation.

get_place_types()[source]
Return a list of all custom place types associated with Place instances in the database.

get_raw_citation_data(handle)[source]
Return raw (serialized and pickled) Citation object from handle

get_raw_event_data(handle)[source]
Return raw (serialized and pickled) Event object from handle

get_raw_family_data(handle)[source]
Return raw (serialized and pickled) Family object from handle

get_raw_media_data(handle)[source]
Return raw (serialized and pickled) Family object from handle

get_raw_note_data(handle)[source]
Return raw (serialized and pickled) Note object from handle

get_raw_person_data(handle)[source]
Return raw (serialized and pickled) Person object from handle

get_raw_place_data(handle)[source]
Return raw (serialized and pickled) Place object from handle

get_raw_repository_data(handle)[source]
Return raw (serialized and pickled) Repository object from handle

get_raw_source_data(handle)[source]
Return raw (serialized and pickled) Source object from handle

get_raw_tag_data(handle)[source]
Return raw (serialized and pickled) Tag object from handle

get_repo_bookmarks()[source]
Return the list of Repository handles in the bookmarks.

get_repository_cursor()[source]
Return a reference to a cursor over Repository objects

get_repository_from_gramps_id(val)[source]
Find a Repository in the database from the passed Gramps ID.

If no such Repository exists, None is returned.

get_repository_from_handle(handle)[source]
Find a Repository in the database from the passed Gramps ID.

If no such Repository exists, a HandleError is raised.

get_repository_handles()[source]
Return a list of database handles, one handle for each Repository in the database.

get_repository_types()[source]
Return a list of all custom repository types associated with Repository instances in the database.

get_researcher()[source]
Return the Researcher instance, providing information about the owner of the database.

get_save_path()[source]
Return the save path of the file, or “” if one does not exist.

get_source_attribute_types()[source]
Return a list of all Attribute types associated with Source/Citation instances in the database.

get_source_bookmarks()[source]
Return the list of Source handles in the bookmarks.

get_source_cursor()[source]
Return a reference to a cursor over Source objects

get_source_from_gramps_id(val)[source]
Find a Source in the database from the passed Gramps ID.

If no such Source exists, None is returned.

get_source_from_handle(handle)[source]
Find a Source in the database from the passed Gramps ID.

If no such Source exists, a HandleError is raised.

get_source_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Source in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Source title.

locale (A GrampsLocale object.) – The locale to use for collation.

get_source_media_types()[source]
Return a list of all custom source media types associated with Source instances in the database.

get_surname_list()[source]
Return the list of locale-sorted surnames contained in the database.

get_tag_cursor()[source]
Return a reference to a cursor over Tag objects

get_tag_from_handle(handle)[source]
Find a Tag in the database from the passed handle.

If no such Tag exists, a HandleError is raised.

get_tag_from_name(val)[source]
Find a Tag in the database from the passed Tag name.

If no such Tag exists, None is returned.

get_tag_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Tag in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Tag name.

locale (A GrampsLocale object.) – The locale to use for collation.

get_url_types()[source]
Return a list of all custom names types associated with Url instances in the database.

has_event_handle(handle)[source]
Return True if the handle exists in the current Event database.

has_family_handle(handle)[source]
Return True if the handle exists in the current Family database.

has_media_handle(handle)[source]
Return True if the handle exists in the current Mediadatabase.

has_name_group_key(name)[source]
Return if a key exists in the name_group table.

has_note_handle(handle)[source]
Return True if the handle exists in the current Note database.

has_person_handle(handle)[source]
Return True if the handle exists in the current Person database.

has_place_handle(handle)[source]
Return True if the handle exists in the current Place database.

has_repository_handle(handle)[source]
Return True if the handle exists in the current Repository database.

has_source_handle(handle)[source]
Return True if the handle exists in the current Source database.

has_tag_handle(handle)[source]
Return True if the handle exists in the current Tag database.

is_open()[source]
Return True if the database has been opened.

iter_citations()[source]
Return an iterator over objects for Citations in the database

iter_event_handles()[source]
Return an iterator over handles for Events in the database

iter_events()[source]
Return an iterator over objects for Events in the database

iter_families()[source]
Return an iterator over objects for Families in the database

iter_family_handles()[source]
Return an iterator over handles for Families in the database

iter_media()[source]
Return an iterator over objects for Medias in the database

iter_media_handles()[source]
Return an iterator over handles for Media in the database

iter_note_handles()[source]
Return an iterator over handles for Notes in the database

iter_notes()[source]
Return an iterator over objects for Notes in the database

iter_people()[source]
Return an iterator over objects for Persons in the database

iter_person_handles()[source]
Return an iterator over handles for Persons in the database

iter_place_handles()[source]
Return an iterator over handles for Places in the database

iter_places()[source]
Return an iterator over objects for Places in the database

iter_repositories()[source]
Return an iterator over objects for Repositories in the database

iter_repository_handles()[source]
Return an iterator over handles for Repositories in the database

iter_source_handles()[source]
Return an iterator over handles for Sources in the database

iter_sources()[source]
Return an iterator over objects for Sources in the database

iter_tag_handles()[source]
Return an iterator over handles for Tags in the database

iter_tags()[source]
Return an iterator over objects for Tags in the database

load(name, callback=None, mode=None, force_schema_upgrade=False, force_bsddb_upgrade=False, force_bsddb_downgrade=False, force_python_upgrade=False, update=True)[source]
Open the specified database.

report_bm_change()[source]
Add 1 to the number of bookmark changes during this session.

request_rebuild()[source]
Notify clients that the data has changed significantly, and that all internal data dependent on the database should be rebuilt. Note that all rebuild signals on all objects are emitted at the same time. It is correct to assume that this is always the case.

Todo it might be better to replace these rebuild signals by one single database-rebuild signal.
set_event_id_prefix(val)[source]
Set the naming template for Gramps Event ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as E%d or E%04d.

set_family_id_prefix(val)[source]
Set the naming template for Gramps Family ID values. The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as F%d or F%04d.

set_feature(feature, value)[source]
Databases can implement certain features.

set_media_id_prefix(val)[source]
Set the naming template for Gramps Media ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as O%d or O%04d.

set_mediapath(path)[source]
Set the default media path for database.

set_note_id_prefix(val)[source]
Set the naming template for Gramps Note ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as N%d or N%04d.

set_person_id_prefix(val)[source]
Set the naming template for Gramps Person ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as I%d or I%04d.

set_place_id_prefix(val)[source]
Set the naming template for Gramps Place ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as P%d or P%04d.

set_prefixes(person, media, family, source, citation, place, event, repository, note)[source]
Set the prefixes for the gramps ids for all gramps objects

set_repository_id_prefix(val)[source]
Set the naming template for Gramps Repository ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as R%d or R%04d.

set_researcher(owner)[source]
Set the information about the owner of the database.

set_source_id_prefix(val)[source]
Set the naming template for Gramps Source ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as S%d or S%04d.

version_supported()[source]
Return True when the file has a supported version.

class gramps.gen.db.dummydb.M_A_M_B[source]
Bases: abc.ABCMeta, gramps.gen.db.dummydb.MetaClass

Metaclass that inherits from two different metaclasses, so as to avoid error: “metaclass conflict: the metaclass of a derived class must be a (non- strict) subclass of the metaclasses of all its bases”

See recipe: http://code.activestate.com/recipes/204197-solving-the- metaclass-conflict/

class gramps.gen.db.dummydb.MetaClass[source]
Bases: type

transform class by wrapping it with a diagnostic wrapper (if __debig__ is not set

gramps.gen.db.dummydb.wrapper(method)[source]
wrapper method that returns a ‘wrapped’ method which can be wrapped round every function in a class. The ‘wrapped’ method logs the original function that was called, and where it was called from.

The gramps.gen.db bsddb Module
Gramps Database API.

Database Architecture
Access to the database is made through Python classes. Exactly what functionality you have is dependent on the properties of the database. For example, if you are accessing a read-only view, then you will only have access to a subset of the methods available.

At the root of any database interface is either DbReadBase and/or DbWriteBase. These define the methods to read and write to a database, respectively.

The full database hierarchy is:

DbBsddb - read and write implementation to BSDDB databases

DbWriteBase - virtual and implementation-independent methods for reading data

DbBsddbRead - read-only (accessors, getters) implementation to BSDDB databases

DbReadBase - virtual and implementation-independent methods for reading data

Callback - callback and signal functions

UpdateCallback - callback functionality

DbBsddb
The DbBsddb interface defines a hierarchical database (non-relational) written in PyBSDDB. There is no such thing as a database schema, and the meaning of the data is defined in the Python classes above. The data is stored as pickled tuples and unserialized into the primary data types (below).

More details can be found in the manual’s Using database API.

GrampsDbRead
Read classes for the Gramps databases.

class gramps.plugins.db.bsddb.read.DbBsddbRead[source]
Bases: gramps.gen.db.base.DbReadBase, gramps.gen.utils.callback.Callback

Read class for the Gramps databases. Implements methods necessary to read the various object classes. Currently, there are nine (9) classes:

Person, Family, Event, Place, Source, Citation, Media, Repository and Note

For each object class, there are methods to retrieve data in various ways. In the methods described below, <object> can be one of person, family, event, place, source, media, respository or note unless otherwise specified.

get_<object>_from_handle()
returns an object given its handle

get_<object>_from_gramps_id()
returns an object given its gramps id

get_<object>_cursor()
returns a cursor over an object. Example use:

with get_person_cursor() as cursor:
    for handle, person in cursor:
        # process person object pointed to by the handle
get_<object>_handles()
returns a list of handles for the object type, optionally sorted (for Citation, Family, Media, Person, Place, Source, and Tag objects)

iter_<object>_handles()
returns an iterator that yields one object handle per call.

iter_<objects>()
returns an iterator that yields one object per call. The objects available are: people, families, events, places, sources, media, repositories and notes.

get_<object>_event_types()
returns a list of all Event types assocated with instances of <object> in the database.

get_<object>_attribute_types()
returns a list of all Event types assocated with instances of <object> in the database.

close()[source]
Close the specified database.

The method needs to be overridden in the derived class.

db_has_bm_changes()[source]
Return whethere there were bookmark changes during the session.

find_backlink_handles(handle, include_classes=None)[source]
Find all objects that hold a reference to the object handle.

Returns an interator over alist of (class_name, handle) tuples.

Parameters
handle (database handle) – handle of the object to search for.

include_classes (list of class names) – list of class names to include in the results. Defaults to None, which includes all classes.

This default implementation does a sequencial scan through all the primary object databases and is very slow. Backends can override this method to provide much faster implementations that make use of additional capabilities of the backend.

Note that this is a generator function, it returns a iterator for use in loops. If you want a list of the results use:

result_list = list(find_backlink_handles(handle))
find_initial_person()[source]
Returns first person in the database

find_next_citation_gramps_id()[source]
Return the next available Gramps ID for a Source object based off the source ID prefix.

find_next_event_gramps_id()[source]
Return the next available Gramps ID for a Event object based off the event ID prefix.

find_next_family_gramps_id()[source]
Return the next available Gramps ID for a Family object based off the family ID prefix.

find_next_media_gramps_id()[source]
Return the next available Gramps ID for a Media object based off the media object ID prefix.

find_next_note_gramps_id()[source]
Return the next available Gramps ID for a Note object based off the note ID prefix.

find_next_person_gramps_id()[source]
Return the next available Gramps ID for a Person object based off the person ID prefix.

find_next_place_gramps_id()[source]
Return the next available Gramps ID for a Place object based off the place ID prefix.

find_next_repository_gramps_id()[source]
Return the next available Gramps ID for a Respository object based off the repository ID prefix.

find_next_source_gramps_id()[source]
Return the next available Gramps ID for a Source object based off the source ID prefix.

get_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_child_reference_types()[source]
Return a list of all child reference types assocated with Family instances in the database.

get_citation_bookmarks()[source]
Return the list of Citation handles in the bookmarks.

get_citation_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Citation objects. Example use:

with get_citation_cursor() as cursor:
for handle, citation in cursor:
# process citation object pointed to by the handle

get_citation_from_gramps_id(val)[source]
Find a Citation in the database from the passed Gramps ID.

If no such Citation exists, None is returned.

get_citation_from_handle(handle)[source]
Find a Citation in the database from the passed handle.

If no such Citation exists, a HandleError is raised.

get_citation_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Citation in the database.

If sort_handles is True, the list is sorted by Citation Volume/Page.

get_dbid()[source]
In BSDDB, we use the file directory name as the unique ID for this database on this computer.

get_dbname()[source]
In BSDDB, the database is in a text file at the path

get_default_handle()[source]
Return the default Person of the database.

get_default_person()[source]
Return the default Person of the database.

get_event_attribute_types()[source]
Return a list of all Attribute types assocated with Event instances in the database.

get_event_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_event_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Family objects. Example use:

with get_event_cursor() as cursor:
for handle, event in cursor:
# process event object pointed to by the handle

get_event_from_gramps_id(val)[source]
Find an Event in the database from the passed Gramps ID.

If no such Family exists, None is returned.

get_event_from_handle(handle)[source]
Find a Event in the database from the passed handle.

If no such Event exists, a HandleError is raised.

get_event_handles()[source]
Return a list of database handles, one handle for each Event in the database.

get_event_roles()[source]
Return a list of all custom event role names assocated with Event instances in the database.

get_event_types()[source]
Return a list of all event types in the database.

get_family_attribute_types()[source]
Return a list of all Attribute types assocated with Family instances in the database.

get_family_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_family_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Family objects. Example use:

with get_family_cursor() as cursor:
for handle, family in cursor:
# process family object pointed to by the handle

get_family_event_types()[source]
Deprecated: Use get_event_types

get_family_from_gramps_id(val)[source]
Find a Family in the database from the passed Gramps ID.

If no such Family exists, None is return.

get_family_from_handle(handle)[source]
Find a Family in the database from the passed handle.

If no such Family exists, a HandleError is raised.

get_family_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Family in the database.

If sort_handles is True, the list is sorted by surnames.

get_family_relation_types()[source]
Return a list of all relationship types assocated with Family instances in the database.

get_media_attribute_types()[source]
Return a list of all Attribute types assocated with Media and MediaRef instances in the database.

get_media_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_media_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Media objects. Example use:

with get_media_cursor() as cursor:
for handle, media in cursor:
# process media object pointed to by the handle

get_media_from_gramps_id(val)[source]
Find a Media in the database from the passed Gramps ID.

If no such Media exists, None is returned.

get_media_from_handle(handle)[source]
Find an Object in the database from the passed handle.

If no such Object exists, a HandleError is raised.

get_media_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Media in the database.

If sort_handles is True, the list is sorted by title.

get_mediapath()[source]
Return the default media path of the database.

get_name_group_keys()[source]
Return the defined names that have been assigned to a default grouping.

get_name_group_mapping(surname)[source]
Return the default grouping name for a surname. Return type is a unicode object

get_name_types()[source]
Return a list of all custom names types assocated with Person instances in the database.

get_note_bookmarks()[source]
Return the list of Note handles in the bookmarks.

get_note_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Note objects. Example use:

with get_note_cursor() as cursor:
for handle, note in cursor:
# process note object pointed to by the handle

get_note_from_gramps_id(val)[source]
Find a Note in the database from the passed Gramps ID.

If no such Note exists, None is returned.

get_note_from_handle(handle)[source]
Find a Note in the database from the passed handle.

If no such Note exists, a HandleError is raised.

get_note_handles()[source]
Return a list of database handles, one handle for each Note in the database.

get_note_types()[source]
Return a list of all custom note types assocated with Note instances in the database.

get_number_of_citations()[source]
Return the number of citations currently in the database.

get_number_of_events()[source]
Return the number of events currently in the database.

get_number_of_families()[source]
Return the number of families currently in the database.

get_number_of_media()[source]
Return the number of media objects currently in the database.

get_number_of_notes()[source]
Return the number of notes currently in the database.

get_number_of_people()[source]
Return the number of people currently in the database.

get_number_of_places()[source]
Return the number of places currently in the database.

get_number_of_repositories()[source]
Return the number of source repositories currently in the database.

get_number_of_sources()[source]
Return the number of sources currently in the database.

get_number_of_tags()[source]
Return the number of tags currently in the database.

get_origin_types()[source]
Return a list of all custom origin types assocated with Person/Surname instances in the database.

get_person_attribute_types()[source]
Return a list of all Attribute types assocated with Person instances in the database.

get_person_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Person objects. Example use:

with get_person_cursor() as cursor:
for handle, person in cursor:
# process person object pointed to by the handle

get_person_event_types()[source]
Deprecated: Use get_event_types

get_person_from_gramps_id(val)[source]
Find a Person in the database from the passed Gramps ID.

If no such Person exists, None is returned.

get_person_from_handle(handle)[source]
Find a Person in the database from the passed handle.

If no such Person exists, a HandleError is raised.

get_person_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Person in the database.

If sort_handles is True, the list is sorted by surnames.

get_place_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_place_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Place objects. Example use:

with get_place_cursor() as cursor:
for handle, place in cursor:
# process place object pointed to by the handle

get_place_from_gramps_id(val)[source]
Find a Place in the database from the passed Gramps ID.

If no such Place exists, None is returned.

get_place_from_handle(handle)[source]
Find a Place in the database from the passed handle.

If no such Place exists, a HandleError is raised.

get_place_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Place in the database.

If sort_handles is True, the list is sorted by Place title.

get_place_tree_cursor(*args, **kwargs)[source]
Return a reference to a cursor that iterates over Place objects in the order they appear in the place hierarchy. Example use:

with get_place_tree_cursor() as cursor:
    for handle, place in cursor:
        # process place object pointed to by the handle
get_place_types()[source]
Return a list of all custom place types assocated with Place instances in the database.

get_raw_citation_data(handle)[source]
Return raw (serialized and pickled) Citation object from handle

get_raw_event_data(handle)[source]
Return raw (serialized and pickled) Event object from handle

get_raw_family_data(handle)[source]
Return raw (serialized and pickled) Family object from handle

get_raw_media_data(handle)[source]
Return raw (serialized and pickled) Family object from handle

get_raw_note_data(handle)[source]
Return raw (serialized and pickled) Note object from handle

get_raw_person_data(handle)[source]
Return raw (serialized and pickled) Person object from handle

get_raw_place_data(handle)[source]
Return raw (serialized and pickled) Place object from handle

get_raw_repository_data(handle)[source]
Return raw (serialized and pickled) Repository object from handle

get_raw_source_data(handle)[source]
Return raw (serialized and pickled) Source object from handle

get_raw_tag_data(handle)[source]
Return raw (serialized and pickled) Tag object from handle

get_repo_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_repository_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Repository objects. Example use:

with get_repository_cursor() as cursor:
for handle, repository in cursor:
# process repository object pointed to by the handle

get_repository_from_gramps_id(val)[source]
Find a Repository in the database from the passed Gramps ID.

If no such Repository exists, None is returned.

get_repository_from_handle(handle)[source]
Find a Repository in the database from the passed handle.

If no such Repository exists, a HandleError is raised.

get_repository_handles()[source]
Return a list of database handles, one handle for each Repository in the database.

get_repository_types()[source]
Return a list of all custom repository types assocated with Repository instances in the database.

get_researcher()[source]
Return the Researcher instance, providing information about the owner of the database.

get_save_path()[source]
Return the save path of the file, or “” if one does not exist.

get_source_attribute_types()[source]
Return a list of all Attribute types assocated with Source/Citation instances in the database.

get_source_bookmarks()[source]
Return the list of Person handles in the bookmarks.

get_source_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Source objects. Example use:

with get_source_cursor() as cursor:
for handle, source in cursor:
# process source object pointed to by the handle

get_source_from_gramps_id(val)[source]
Find a Source in the database from the passed Gramps ID.

If no such Source exists, None is returned.

get_source_from_handle(handle)[source]
Find a Source in the database from the passed handle.

If no such Source exists, a HandleError is raised.

get_source_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Source in the database.

If sort_handles is True, the list is sorted by Source title.

get_source_media_types()[source]
Return a list of all custom source media types assocated with Source instances in the database.

get_summary()[source]
Returns dictionary of summary item. Should include, if possible:

_(“Number of people”) _(“Version”) _(“Schema version”)

get_surname_list()[source]
Return the list of locale-sorted surnames contained in the database.

get_tag_cursor(*args, **kwargs)[source]
Return a reference to a cursor over Tag objects. Example use:

with get_tag_cursor() as cursor:
for handle, tag in cursor:
# process tag object pointed to by the handle

get_tag_from_handle(handle)[source]
Find a Tag in the database from the passed handle.

If no such Tag exists, a HandleError is raised.

get_tag_from_name(val)[source]
Find a Tag in the database from the passed Tag name.

If no such Tag exists, None is returned.

get_tag_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Tag in the database.

If sort_handles is True, the list is sorted by Tag name.

get_url_types()[source]
Return a list of all custom names types assocated with Url instances in the database.

has_citation_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Citation table.

has_citation_handle(handle)[source]
Return True if the handle exists in the current Citation database.

has_event_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Event table.

has_event_handle(handle)[source]
Return True if the handle exists in the current Event database.

has_family_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Family table.

has_family_handle(handle)[source]
Return True if the handle exists in the current Family database.

has_media_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Media table.

has_media_handle(handle)[source]
Return True if the handle exists in the current Mediadatabase.

has_name_group_key(name)[source]
Return if a key exists in the name_group table.

has_note_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Note table.

has_note_handle(handle)[source]
Return True if the handle exists in the current Note database.

has_person_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Person table.

has_person_handle(handle)[source]
Return True if the handle exists in the current Person database.

has_place_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Place table.

has_place_handle(handle)[source]
Return True if the handle exists in the current Place database.

has_repository_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Repository table.

has_repository_handle(handle)[source]
Return True if the handle exists in the current Repository database.

has_source_gramps_id(gramps_id)[source]
Return True if the Gramps ID exists in the Source table.

has_source_handle(handle)[source]
Return True if the handle exists in the current Source database.

has_tag_handle(handle)[source]
Return True if the handle exists in the current Tag database.

is_empty()[source]
Return true if there are no [primary] records in the database

is_open()[source]
Return 1 if the database has been opened.

report_bm_change()[source]
Add 1 to the number of bookmark changes during this session.

request_rebuild()[source]
Notify clients that the data has changed significantly, and that all internal data dependent on the database should be rebuilt.

set_citation_id_prefix(val)[source]
Set the naming template for Gramps Citation ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as C%d or C%04d.

set_event_id_prefix(val)[source]
Set the naming template for Gramps Event ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as E%d or E%04d.

set_family_id_prefix(val)[source]
Set the naming template for Gramps Family ID values. The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as F%d or F%04d.

set_media_id_prefix(val)[source]
Set the naming template for Gramps Media ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as O%d or O%04d.

set_mediapath(path)[source]
Set the default media path for database.

set_note_id_prefix(val)[source]
Set the naming template for Gramps Note ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as N%d or N%04d.

set_person_id_prefix(val)[source]
Set the naming template for Gramps Person ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as I%d or I%04d.

set_place_id_prefix(val)[source]
Set the naming template for Gramps Place ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as P%d or P%04d.

set_prefixes(person, media, family, source, citation, place, event, repository, note)[source]
Set the prefixes for the gramps ids for all gramps objects

set_repository_id_prefix(val)[source]
Set the naming template for Gramps Repository ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as R%d or R%04d.

set_researcher(owner)[source]
Set the information about the owner of the database.

set_source_id_prefix(val)[source]
Set the naming template for Gramps Source ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as S%d or S%04d.

version_supported()[source]
Return True when the file has a supported version.

class gramps.plugins.db.bsddb.read.DbBsddbTreeCursor(source, primary, readonly, txn=None, **kwargs)[source]
Bases: gramps.plugins.db.bsddb.cursor.BsddbBaseCursor

class gramps.plugins.db.bsddb.read.DbReadCursor(source, txn=None, **kwargs)[source]
Bases: gramps.plugins.db.bsddb.cursor.BsddbBaseCursor

gramps.plugins.db.bsddb.read.find_byte_surname(key, data)[source]
Creating a surname from raw data of a person, to use for sort and index returns a byte string

gramps.plugins.db.bsddb.read.find_fullname(key, data)[source]
Creating a fullname from raw data of a person, to use for sort and index

gramps.plugins.db.bsddb.read.find_surname(key, data)[source]
Creating a surname from raw data of a person, to use for sort and index

gramps.plugins.db.bsddb.read.find_surname_name(key, data)[source]
Creating a surname from raw name, to use for sort and index

GrampsDbWrite
Provide the Berkeley DB (DbBsddb) database backend for Gramps. This is used since Gramps version 3.0

class gramps.plugins.db.bsddb.write.BsddbWriteCursor(source, txn=None, **kwargs)[source]
Bases: gramps.plugins.db.bsddb.cursor.BsddbBaseCursor

class gramps.plugins.db.bsddb.write.DbBsddb[source]
Bases: gramps.plugins.db.bsddb.read.DbBsddbRead, gramps.gen.db.base.DbWriteBase, gramps.gen.updatecallback.UpdateCallback

Gramps database write access object.

add_citation(citation, transaction, set_gid=True)[source]
Add a Citation to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_event(event, transaction, set_gid=True)[source]
Add an Event to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_family(family, transaction, set_gid=True)[source]
Add a Family to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_media(media, transaction, set_gid=True)[source]
Add a Media to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_note(obj, transaction, set_gid=True)[source]
Add a Note to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_person(person, transaction, set_gid=True)[source]
Add a Person to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_place(place, transaction, set_gid=True)[source]
Add a Place to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_repository(obj, transaction, set_gid=True)[source]
Add a Repository to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_source(source, transaction, set_gid=True)[source]
Add a Source to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_tag(obj, transaction)[source]
Add a Tag to the database, assigning a handle if it has not already been defined.

add_to_surname_list(person, batch_transaction)[source]
Add surname to surname list

catch_db_error()[source]
Decorator function for catching database errors. If func throws one of the exceptions in DBERRS, the error is logged and a DbError exception is raised.

close(update=True, user=None)[source]
Close the database. if update is False, don’t change access times, etc.

commit_citation(citation, transaction, change_time=None)[source]
Commit the specified Citation to the database, storing the changes as part of the transaction.

commit_event(event, transaction, change_time=None)[source]
Commit the specified Event to the database, storing the changes as part of the transaction.

commit_family(family, transaction, change_time=None)[source]
Commit the specified Family to the database, storing the changes as part of the transaction.

commit_media(obj, transaction, change_time=None)[source]
Commit the specified Media to the database, storing the changes as part of the transaction.

commit_note(note, transaction, change_time=None)[source]
Commit the specified Note to the database, storing the changes as part of the transaction.

commit_person(person, transaction, change_time=None)[source]
Commit the specified Person to the database, storing the changes as part of the transaction.

commit_place(place, transaction, change_time=None)[source]
Commit the specified Place to the database, storing the changes as part of the transaction.

commit_repository(repository, transaction, change_time=None)[source]
Commit the specified Repository to the database, storing the changes as part of the transaction.

commit_source(source, transaction, change_time=None)[source]
Commit the specified Source to the database, storing the changes as part of the transaction.

commit_tag(tag, transaction, change_time=None)[source]
Commit the specified Tag to the database, storing the changes as part of the transaction.

find_backlink_handles(handle, include_classes=None)[source]
Find all objects that hold a reference to the object handle.

Returns an interator over a list of (class_name, handle) tuples.

Parameters
handle (database handle) – handle of the object to search for.

include_classes (list of class names) – list of class names to include in the results. Default: None means include all classes.

Note that this is a generator function, it returns a iterator for use in loops. If you want a list of the results use:

result_list = list(find_backlink_handles(handle))
find_place_child_handles(handle)[source]
Find all child places having the given place as the primary parent.

get_cursor(table, txn=None, update=False, commit=False)[source]
Helper function to return a cursor over a table

get_dbid()[source]
In BSDDB, we use the file directory name as the unique ID for this database on this computer.

get_default_person()[source]
Return the default Person of the database.

get_from_handle(handle, class_type, data_map)[source]
get_place_parent_cursor()[source]
Returns a reference to a cursor over the place parents

get_summary()[source]
Returns dictionary of summary item. Should include, if possible:

_(“Number of people”) _(“Version”) _(“Schema version”)

get_undodb()[source]
Return the database that keeps track of Undo/Redo operations.

load(name, callback=None, mode='w', force_schema_upgrade=False, force_bsddb_upgrade=False, force_bsddb_downgrade=False, force_python_upgrade=False, update=True, username=None, password=None)[source]
If update is False: then don’t update any files; open read-only

rebuild_secondary(callback=None)[source]
Rebuild secondary indices

redo(update_history=True)[source]
Redo last transaction.

reindex_reference_map(callback)[source]
Reindex all primary records in the database.

This will be a slow process for large databases.

remove_citation(handle, transaction)[source]
Remove the Citation specified by the database handle from the database, preserving the change in the passed transaction.

remove_event(handle, transaction)[source]
Remove the Event specified by the database handle from the database, preserving the change in the passed transaction.

remove_family(handle, transaction)[source]
Remove the Family specified by the database handle from the database, preserving the change in the passed transaction.

remove_from_surname_list(person)[source]
Check whether there are persons with the same surname left in the database.

If not then we need to remove the name from the list. The function must be overridden in the derived class.

remove_media(handle, transaction)[source]
Remove the MediaPerson specified by the database handle from the database, preserving the change in the passed transaction.

remove_note(handle, transaction)[source]
Remove the Note specified by the database handle from the database, preserving the change in the passed transaction.

remove_person(handle, transaction)[source]
Remove the Person specified by the database handle from the database, preserving the change in the passed transaction.

remove_place(handle, transaction)[source]
Remove the Place specified by the database handle from the database, preserving the change in the passed transaction.

remove_repository(handle, transaction)[source]
Remove the Repository specified by the database handle from the database, preserving the change in the passed transaction.

remove_source(handle, transaction)[source]
Remove the Source specified by the database handle from the database, preserving the change in the passed transaction.

remove_tag(handle, transaction)[source]
Remove the Tag specified by the database handle from the database, preserving the change in the passed transaction.

set_default_person_handle(handle)[source]
Set the default Person to the passed instance.

set_mediapath(path)[source]
Set the default media path for database.

set_name_group_mapping(name, group)[source]
Set the default grouping name for a surname.

Needs to be overridden in the derived class.

transaction_abort(transaction)[source]
Revert the changes made to the database so far during the transaction.

transaction_begin(transaction)[source]
Prepare the database for the start of a new Transaction.

Supported transaction parameters:

no_magic
Boolean, defaults to False, indicating if secondary indices should be disconnected.

transaction_commit(transaction)[source]
Make the changes to the database final and add the content of the transaction to the undo database.

undo(update_history=True)[source]
Undo last transaction.

version_supported()[source]
Return True when the file has a supported version.

class gramps.plugins.db.bsddb.write.DbBsddbAssocCursor(source, txn=None, **kwargs)[source]
Bases: gramps.plugins.db.bsddb.cursor.BsddbBaseCursor

gramps.plugins.db.bsddb.write.find_idmap(key, data)[source]
return id for association of secondary index. returns a byte string

gramps.plugins.db.bsddb.write.find_parent(key, data)[source]
gramps.plugins.db.bsddb.write.find_primary_handle(key, data)[source]
return handle for association of indexes returns byte string

gramps.plugins.db.bsddb.write.find_referenced_handle(key, data)[source]
return handle for association of indexes returns byte string

gramps.plugins.db.bsddb.write.upgrade_researcher(owner_data)[source]
Upgrade researcher data to include a locality field in the address. This should be called for databases prior to Gramps 3.3.

GrampsCursor
class gramps.plugins.db.bsddb.cursor.BsddbBaseCursor(txn=None, update=False, commit=False)[source]
Bases: object

Provide a basic iterator that allows the user to cycle through the elements in a particular map.

A cursor should never be directly instantiated. Instead, in should be created by the database class.

A cursor should only be used for a single pass through the database. If multiple passes are needed, multiple cursors should be used.

current(flags=0, **kwargs)
Issue DBCursor get call (with DB_RMW flag if update requested) Return results to caller

first(flags=0, **kwargs)
Issue DBCursor get call (with DB_RMW flag if update requested) Return results to caller

last(flags=0, **kwargs)
Issue DBCursor get call (with DB_RMW flag if update requested) Return results to caller

next(flags=0, **kwargs)
Issue DBCursor get call (with DB_RMW flag if update requested) Return results to caller

prev(flags=0, **kwargs)
Issue DBCursor get call (with DB_RMW flag if update requested) Return results to caller

update(key, data, flags=0, **kwargs)[source]
Write the current key, data pair to the database.

BSDDBtxn
BSDDBTxn class: Wrapper for BSDDB transaction-oriented methods

class gramps.plugins.db.bsddb.bsddbtxn.BSDDBTxn(env, db=None)[source]
Bases: object

Wrapper for BSDDB methods that set up and manage transactions. Implements context management functionality allowing constructs like:

with BSDDBTxn(env) as txn:
DB.get(txn=txn) DB.put(txn=txn) DB.delete(txn=txn)

and other transaction-oriented DB access methods, where “env” is a BSDDB DBEnv object and “DB” is a BSDDB database object.

Transactions are automatically begun when the “with” statement is executed and automatically committed when control flows off the end of the “with” statement context, either implicitly by reaching the end of the indentation level or explicity if a “return” statement is encountered or an exception is raised.

abort()[source]
Abort the transaction

begin(*args, **kwargs)[source]
Create and begin a new transaction. A DBTxn object is returned

checkpoint(*args, **kwargs)[source]
Flush the underlying memory pool, write a checkpoint record to the log and then flush the log

commit(flags=0)[source]
End the transaction, committing any changes to the databases

db
delete(key, txn=None, **kwargs)[source]
Removes a key/data pair from the database

discard()[source]
Release all the per-process resources associated with the specified transaction, neither committing nor aborting the transaction

env
get(key, default=None, txn=None, **kwargs)[source]
Returns the data object associated with key

id()[source]
Return the unique transaction id associated with the specified transaction

parent
pget(key, default=None, txn=None, **kwargs)[source]
Returns the primary key, given the secondary one, and associated data

prepare(gid)[source]
Initiate the beginning of a two-phase commit

put(key, data, txn=None, **kwargs)[source]
Stores the key/data pair in the database

recover()[source]
Returns a list of tuples (GID, TXN) of transactions prepared but still unresolved

stat()[source]
Return a dictionary of transaction statistics

txn
The gramps.gen.db dbapi Module
DBAPI
class gramps.plugins.db.dbapi.dbapi.DBAPI(directory=None)[source]
Bases: gramps.gen.db.generic.DbGeneric

Database backends class for DB-API 2.0 databases

find_backlink_handles(handle, include_classes=None)[source]
Find all objects that hold a reference to the object handle.

Returns an interator over a list of (class_name, handle) tuples.

Parameters
handle (database handle) – handle of the object to search for.

include_classes (list of class names) – list of class names to include in the results. Default: None means include all classes.

Note that this is a generator function, it returns a iterator for use in loops. If you want a list of the results use:

result_list = list(find_backlink_handles(handle))
find_initial_person()[source]
Returns first person in the database

get_citation_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Citation in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Citation title.

locale (A GrampsLocale object.) – The locale to use for collation.

get_event_handles()[source]
Return a list of database handles, one handle for each Event in the database.

get_family_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Family in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by surnames.

locale (A GrampsLocale object.) – The locale to use for collation.

get_gender_stats()[source]
Returns a dictionary of {given_name: (male_count, female_count, unknown_count)}

get_media_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Media in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by title.

locale (A GrampsLocale object.) – The locale to use for collation.

get_name_group_keys()[source]
Return the defined names that have been assigned to a default grouping.

get_name_group_mapping(key)[source]
Return the default grouping name for a surname.

get_note_handles()[source]
Return a list of database handles, one handle for each Note in the database.

get_person_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Person in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by surnames.

locale (A GrampsLocale object.) – The locale to use for collation.

get_place_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Place in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Place title.

locale (A GrampsLocale object.) – The locale to use for collation.

get_repository_handles()[source]
Return a list of database handles, one handle for each Repository in the database.

get_source_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Source in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Source title.

locale (A GrampsLocale object.) – The locale to use for collation.

get_surname_list()[source]
Return the list of locale-sorted surnames contained in the database.

get_tag_from_name(name)[source]
Find a Tag in the database from the passed Tag name.

If no such Tag exists, None is returned.

get_tag_handles(sort_handles=False, locale=<gramps.gen.utils.grampslocale.GrampsLocale object>)[source]
Return a list of database handles, one handle for each Tag in the database.

Parameters
sort_handles (bool) – If True, the list is sorted by Tag name.

locale (A GrampsLocale object.) – The locale to use for collation.

has_name_group_key(key)[source]
Return if a key exists in the name_group table.

rebuild_secondary(callback=None)[source]
Rebuild secondary indices

reindex_reference_map(callback)[source]
Reindex all primary records in the database.

set_name_group_mapping(name, grouping)[source]
Set the default grouping name for a surname.

transaction_abort(txn)[source]
Executed after a batch operation abort.

transaction_begin(transaction)[source]
Transactions are handled automatically by the db layer.

transaction_commit(txn)[source]
Executed at the end of a transaction.

undo_data(data, handle, obj_key)[source]
Helper method to undo/redo the changes made

undo_reference(data, handle)[source]
Helper method to undo a reference map entry

Sqlite
Backend for SQLite database.

class gramps.plugins.db.dbapi.sqlite.Connection(*args, **kwargs)[source]
Bases: object

The Sqlite class is an interface between the DBAPI class which is the Gramps backend for the DBAPI interface and the sqlite3 python module.

begin()[source]
Start a transaction manually. This transactions usually persist until the next COMMIT or ROLLBACK command.

check_collation(locale)[source]
Checks that a collation exists and if not creates it.

Parameters
locale – Locale to be checked.

type – A GrampsLocale object.

close()[source]
Close the current database.

commit()[source]
Commit the current transaction.

cursor()[source]
Return a new cursor.

execute(*args, **kwargs)[source]
Executes an SQL statement.

Parameters
args (list) – arguments to be passed to the sqlite3 execute statement

kwargs (list) – arguments to be passed to the sqlite3 execute statement

fetchall()[source]
Fetches the next set of rows of a query result, returning a list. An empty list is returned when no more rows are available.

fetchone()[source]
Fetches the next row of a query result set, returning a single sequence, or None when no more data is available.

rollback()[source]
Roll back any changes to the database since the last call to commit().

table_exists(table)[source]
Test whether the specified SQL database table exists.

Parameters
table (str) – table name to check.

Returns
True if the table exists, false otherwise.

Return type
bool

class gramps.plugins.db.dbapi.sqlite.SQLite(directory=None)[source]
Bases: gramps.plugins.db.dbapi.dbapi.DBAPI

get_summary()[source]
Return a dictionary of information about this database backend.

gramps.plugins.db.dbapi.sqlite.regexp(expr, value)[source]
A user defined function that can be called from within an SQL statement.

This function has two parameters.

Parameters
expr (str) – pattern to look for.

value (list) – the string to search.

Returns
True if the expr exists within the value, false otherwise.

Return type
bool

Table of Contents
The gramps.gen.db Module
Database Architecture
DbBsddb
GrampsDbBase
GrampsDbTxn
DbConst
GrampsDbException
GrampsDbUndo
Generic
DummyDb
The gramps.gen.db bsddb Module
Database Architecture
DbBsddb
GrampsDbRead
GrampsDbWrite
GrampsCursor
BSDDBtxn
The gramps.gen.db dbapi Module
DBAPI
Sqlite
Previous topic
The gramps.gen Module

Next topic
The gramps.gen.display Module

This Page
Show Source
Quick search
indexmodules |next |previous |Gramps 5.1.0 documentation » Code Documentation »
© Copyright 2001-2019, The Gramps Project. Created using Sphinx 2.0.1.