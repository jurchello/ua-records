https://gramps-project.org/api_3_3_x/gen/gen_db.html


The gen.db Module
Gramps Database API.

Database Architecture
Access to the database is made through Python classes. Exactly what functionality you have is dependent on the properties of the database. For example, if you are accessing a read-only view, then you will only have access to a subset of the methods available.

At the root of any database interface is either DbReadBase and/or DbWriteBase. These define the methods to read and write to a database, respectively.

The full database hierarchy is:

B{DbBsddb} - read and write implementation to BSDDB databases (U{gen/db/write<http://gramps.svn.sourceforge.net/viewvc/gramps/trunk/src/gen/db/write.py?view=markup>})
B{DbWriteBase} - virtual and implementation-independent methods for reading data (U{gen/db/base.py<http://gramps.svn.sourceforge.net/viewvc/gramps/trunk/src/gen/db/base.py?view=markup>})

B{DbBsddbRead} - read-only (accessors, getters) implementation to BSDDB databases (U{gen/db/read.py<http://gramps.svn.sourceforge.net/viewvc/gramps/trunk/src/gen/db/read.py?view=markup})
B{DbReadBase} - virtual and implementation-independent methods for reading data (U{gen/db/base.py<http://gramps.svn.sourceforge.net/viewvc/gramps/trunk/src/gen/db/base.py?view=markup})
B{Callback} - callback and signal functions (U{gen/utils/callback.py<http://gramps.svn.sourceforge.net/viewvc/gramps/trunk/src/gen/utils/callback.py?view=markup})
B{UpdateCallback} - callback functionality (U{gen/updatecallback.py<http://gramps.svn.sourceforge.net/viewvc/gramps/trunk/src/gen/db/read.py?view=markup gen/updatecallback.py?view=markup>})

B{DbDjango} - read and write implementation to Django-based databases (U{web/dbdjango.py<http://gramps.svn.sourceforge.net/viewvc/gramps/trunk/src/web/dbdjango.py?view=markup})
B{DbWriteBase} - virtual and implementation-independent methods for reading data (U{gen/db/base.py<http://gramps.svn.sourceforge.net/viewvc/gramps/trunk/src/gen/db/base.py?view=markup})
B{DbReadBase} - virtual and implementation-independent methods for reading data (U{gen/db/base.py<http://gramps.svn.sourceforge.net/viewvc/gramps/trunk/src/gen/db/base.py?view=markup})
DbBsddb
The DbBsddb interface defines a hierarchical database (non-relational) written in U{http://www.jcea.es/programacion/pybsddb.htm PyBSDDB}. There is no such thing as a database schema, and the meaning of the data is defined in the Python classes above. The data is stored as pickled tuples and unserialized into the primary data types (below).

DbDjango
The DbDjango interface defines the Gramps data in terms of I{models} and I{relations} from the U{Django project<http://www.djangoproject.com/}. The database backend can be any implementation that supports Django, including such popular SQL implementations as sqlite, MySQL, Postgresql, and Oracle. The data is retrieved from the SQL fields, serialized and then unserialized into the primary data types (below).

More details can be found in the manual’s U{Using database API<http://www.gramps-project.org/wiki/index.php?title=Using_database_API>}.

GrampsDbBase
Base class for the GRAMPS databases. All database interfaces should inherit from this class.

class gen.db.base.DbReadBase
Bases: object

GRAMPS database object. This object is a base class for all database interfaces. All methods raise NotImplementedError and must be implemented in the derived class as required.

all_handles(table)
Return all handles from the specified table as a list

close()
Close the specified database.

create_id()
Create an id

db_has_bm_changes()
Return whethere there were bookmark changes during the session.

find_backlink_handles(handle, include_classes=None)
Find all objects that hold a reference to the object handle.

Returns an iterator over a list of (class_name, handle) tuples.

Parameters:	
handle (database handle) – handle of the object to search for.
include_classes (list of class names) – list of class names to include in the results. Default is None which includes all classes.
This default implementation does a sequential scan through all the primary object databases and is very slow. Backends can override this method to provide much faster implementations that make use of additional capabilities of the backend.

Note that this is a generator function, it returns a iterator for use in loops. If you want a list of the results use:

result_list = list(find_backlink_handles(handle))
find_initial_person()
Returns first person in the database

find_next_event_gramps_id()
Return the next available GRAMPS’ ID for a Event object based off the event ID prefix.

find_next_family_gramps_id()
Return the next available GRAMPS’ ID for a Family object based off the family ID prefix.

find_next_note_gramps_id()
Return the next available GRAMPS’ ID for a Note object based off the note ID prefix.

find_next_object_gramps_id()
Return the next available GRAMPS’ ID for a MediaObject object based off the media object ID prefix.

find_next_person_gramps_id()
Return the next available GRAMPS’ ID for a Person object based off the person ID prefix.

find_next_place_gramps_id()
Return the next available GRAMPS’ ID for a Place object based off the place ID prefix.

find_next_repository_gramps_id()
Return the next available GRAMPS’ ID for a Repository object based off the repository ID prefix.

find_next_source_gramps_id()
Return the next available GRAMPS’ ID for a Source object based off the source ID prefix.

get_bookmarks()
Return the list of Person handles in the bookmarks.

get_child_reference_types()
Return a list of all child reference types associated with Family instances in the database.

get_dbid()
A unique ID for this database on this computer.

get_dbname()
A name for this database on this computer.

get_default_handle()
Return the default Person of the database.

get_default_person()
Return the default Person of the database.

get_event_bookmarks()
Return the list of Person handles in the bookmarks.

get_event_cursor()
Return a reference to a cursor over Family objects

get_event_from_gramps_id(val)
Find an Event in the database from the passed GRAMPS ID.

If no such Event exists, None is returned. Needs to be overridden by the derived class.

get_event_from_handle(handle)
Find a Event in the database from the passed gramps’ ID.

If no such Event exists, None is returned.

get_event_handles()
Return a list of database handles, one handle for each Event in the database.

get_event_roles()
Return a list of all custom event role names associated with Event instances in the database.

get_family_attribute_types()
Return a list of all Attribute types associated with Family instances in the database.

get_family_bookmarks()
Return the list of Person handles in the bookmarks.

get_family_cursor()
Return a reference to a cursor over Family objects

get_family_event_types()
Return a list of all Event types associated with Family instances in the database.

get_family_from_gramps_id(val)
Find a Family in the database from the passed GRAMPS ID.

If no such Family exists, None is returned. Need to be overridden by the derived class.

get_family_from_handle(handle)
Find a Family in the database from the passed gramps’ ID.

If no such Family exists, None is returned.

get_family_handles()
Return a list of database handles, one handle for each Family in the database.

get_family_relation_types()
Return a list of all relationship types associated with Family instances in the database.

get_from_handle(handle, class_type, data_map)
Return unserialized data from database given handle and object class

get_gramps_ids(obj_key)
Returns all the keys from a table given a table name

get_media_attribute_types()
Return a list of all Attribute types associated with Media and MediaRef instances in the database.

get_media_bookmarks()
Return the list of Person handles in the bookmarks.

get_media_cursor()
Return a reference to a cursor over Media objects

get_media_object_handles(sort_handles=False)
Return a list of database handles, one handle for each MediaObject in the database.

If sort_handles is True, the list is sorted by title.

get_mediapath()
Return the default media path of the database.

get_name_group_keys()
Return the defined names that have been assigned to a default grouping.

get_name_group_mapping(surname)
Return the default grouping name for a surname.

get_name_types()
Return a list of all custom names types associated with Person instances in the database.

get_note_bookmarks()
Return the list of Note handles in the bookmarks.

get_note_cursor()
Return a reference to a cursor over Note objects

get_note_from_gramps_id(val)
Find a Note in the database from the passed gramps’ ID.

If no such Note exists, None is returned. Needs to be overridden by the derived classderri.

get_note_from_handle(handle)
Find a Note in the database from the passed gramps’ ID.

If no such Note exists, None is returned.

get_note_handles()
Return a list of database handles, one handle for each Note in the database.

get_note_types()
Return a list of all custom note types associated with Note instances in the database.

get_number_of_events()
Return the number of events currently in the database.

get_number_of_families()
Return the number of families currently in the database.

get_number_of_media_objects()
Return the number of media objects currently in the database.

get_number_of_notes()
Return the number of notes currently in the database.

get_number_of_people()
Return the number of people currently in the database.

get_number_of_places()
Return the number of places currently in the database.

get_number_of_repositories()
Return the number of source repositories currently in the database.

get_number_of_sources()
Return the number of sources currently in the database.

get_number_of_tags()
Return the number of tags currently in the database.

get_object_from_gramps_id(val)
Find a MediaObject in the database from the passed gramps’ ID.

If no such MediaObject exists, None is returned. Needs to be overridden by the derived class.

get_object_from_handle(handle)
Find an Object in the database from the passed gramps’ ID.

If no such Object exists, None is returned.

get_origin_types()
Return a list of all custom origin types associated with Person/Surname instances in the database.

get_person_attribute_types()
Return a list of all Attribute types associated with Person instances in the database.

get_person_cursor()
Return a reference to a cursor over Person objects

get_person_event_types()
Return a list of all Event types associated with Person instances in the database.

get_person_from_gramps_id(val)
Find a Person in the database from the passed GRAMPS ID.

If no such Person exists, None is returned. Needs to be overridden by the derived class.

get_person_from_handle(handle)
Find a Person in the database from the passed gramps’ ID.

If no such Person exists, None is returned.

get_person_handles(sort_handles=False)
Return a list of database handles, one handle for each Person in the database.

If sort_handles is True, the list is sorted by surnames.

get_place_bookmarks()
Return the list of Person handles in the bookmarks.

get_place_cursor()
Return a reference to a cursor over Place objects

get_place_from_gramps_id(val)
Find a Place in the database from the passed gramps’ ID.

If no such Place exists, None is returned. Needs to be overridden by the derived class.

get_place_from_handle(handle)
Find a Place in the database from the passed gramps’ ID.

If no such Place exists, None is returned.

get_place_handles(sort_handles=False)
Return a list of database handles, one handle for each Place in the database.

If sort_handles is True, the list is sorted by Place title.

get_raw_event_data(handle)
Return raw (serialized and pickled) Event object from handle

get_raw_family_data(handle)
Return raw (serialized and pickled) Family object from handle

get_raw_note_data(handle)
Return raw (serialized and pickled) Note object from handle

get_raw_object_data(handle)
Return raw (serialized and pickled) Family object from handle

get_raw_person_data(handle)
Return raw (serialized and pickled) Person object from handle

get_raw_place_data(handle)
Return raw (serialized and pickled) Place object from handle

get_raw_repository_data(handle)
Return raw (serialized and pickled) Repository object from handle

get_raw_source_data(handle)
Return raw (serialized and pickled) Source object from handle

get_raw_tag_data(handle)
Return raw (serialized and pickled) Tag object from handle

get_reference_map_cursor()
Returns a reference to a cursor over the reference map

get_reference_map_primary_cursor()
Returns a reference to a cursor over the reference map primary map

get_reference_map_referenced_cursor()
Returns a reference to a cursor over the reference map referenced map

get_repo_bookmarks()
Return the list of Person handles in the bookmarks.

get_repository_cursor()
Return a reference to a cursor over Repository objects

get_repository_from_gramps_id(val)
Find a Repository in the database from the passed gramps’ ID.

If no such Repository exists, None is returned. Needs to be overridden by the derived class.

get_repository_from_handle(handle)
Find a Repository in the database from the passed gramps’ ID.

If no such Repository exists, None is returned.

get_repository_handles()
Return a list of database handles, one handle for each Repository in the database.

get_repository_types()
Return a list of all custom repository types associated with Repository instances in the database.

get_researcher()
Return the Researcher instance, providing information about the owner of the database.

get_save_path()
Return the save path of the file, or “” if one does not exist.

get_source_bookmarks()
Return the list of Person handles in the bookmarks.

get_source_cursor()
Return a reference to a cursor over Source objects

get_source_from_gramps_id(val)
Find a Source in the database from the passed gramps’ ID.

If no such Source exists, None is returned. Needs to be overridden by the derived class.

get_source_from_handle(handle)
Find a Source in the database from the passed gramps’ ID.

If no such Source exists, None is returned.

get_source_handles(sort_handles=False)
Return a list of database handles, one handle for each Source in the database.

If sort_handles is True, the list is sorted by Source title.

get_source_media_types()
Return a list of all custom source media types associated with Source instances in the database.

get_surname_list()
Return the list of locale-sorted surnames contained in the database.

get_tag_cursor()
Return a reference to a cursor over Tag objects

get_tag_from_handle(handle)
Find a Tag in the database from the passed handle.

If no such Tag exists, None is returned.

get_tag_from_name(val)
Find a Tag in the database from the passed Tag name.

If no such Tag exists, None is returned. Needs to be overridden by the derived class.

get_tag_handles(sort_handles=False)
Return a list of database handles, one handle for each Tag in the database.

If sort_handles is True, the list is sorted by Tag name.

get_url_types()
Return a list of all custom names types associated with Url instances in the database.

gramps_upgrade()
Return True if database is upgraded

has_event_handle(handle)
Return True if the handle exists in the current Event database.

has_family_handle(handle)
Return True if the handle exists in the current Family database.

has_gramps_id(obj_key, gramps_id)
Returns True if the key exists in table given a table name

Not used in current codebase

has_name_group_key(name)
Return if a key exists in the name_group table.

has_note_handle(handle)
Return True if the handle exists in the current Note database.

has_object_handle(handle)
Return True if the handle exists in the current MediaObjectdatabase.

has_person_handle(handle)
Return True if the handle exists in the current Person database.

has_place_handle(handle)
Return True if the handle exists in the current Place database.

has_repository_handle(handle)
Return True if the handle exists in the current Repository database.

has_source_handle(handle)
Return True if the handle exists in the current Source database.

has_tag_handle(handle)
Return True if the handle exists in the current Tag database.

is_open()
Return True if the database has been opened.

iter_event_handles()
Return an iterator over handles for Events in the database

iter_events()
Return an iterator over objects for Events in the database

iter_families()
Return an iterator over objects for Families in the database

iter_family_handles()
Return an iterator over handles for Families in the database

iter_media_object_handles()
Return an iterator over handles for Media in the database

iter_media_objects()
Return an iterator over objects for MediaObjects in the database

iter_note_handles()
Return an iterator over handles for Notes in the database

iter_notes()
Return an iterator over objects for Notes in the database

iter_people()
Return an iterator over objects for Persons in the database

iter_person_handles()
Return an iterator over handles for Persons in the database

iter_place_handles()
Return an iterator over handles for Places in the database

iter_places()
Return an iterator over objects for Places in the database

iter_repositories()
Return an iterator over objects for Repositories in the database

iter_repository_handles()
Return an iterator over handles for Repositories in the database

iter_source_handles()
Return an iterator over handles for Sources in the database

iter_sources()
Return an iterator over objects for Sources in the database

iter_tag_handles()
Return an iterator over handles for Tags in the database

iter_tags()
Return an iterator over objects for Tags in the database

load(name, callback, mode=None, upgrade=False)
Open the specified database.

report_bm_change()
Add 1 to the number of bookmark changes during this session.

request_rebuild()
Notify clients that the data has changed significantly, and that all internal data dependent on the database should be rebuilt. Note that all rebuild signals on all objects are emitted at the same time. It is correct to assume that this is always the case. TODO: it might be better to replace these rebuild signals by one single

database-rebuild signal.
set_event_id_prefix(val)
Set the naming template for GRAMPS Event ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as E%d or E%04d.

set_family_id_prefix(val)
Set the naming template for GRAMPS Family ID values. The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as F%d or F%04d.

set_mediapath(path)
Set the default media path for database, path should be utf-8.

set_note_id_prefix(val)
Set the naming template for GRAMPS Note ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as N%d or N%04d.

set_object_id_prefix(val)
Set the naming template for GRAMPS MediaObject ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as O%d or O%04d.

set_person_id_prefix(val)
Set the naming template for GRAMPS Person ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as I%d or I%04d.

set_place_id_prefix(val)
Set the naming template for GRAMPS Place ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as P%d or P%04d.

set_prefixes(person, media, family, source, place, event, repository, note)
Set the prefixes for the gramps ids for all gramps objects

set_redo_callback(callback)
Define the callback function that is called whenever an redo operation is executed.

The callback function receives a single argument that is a text string that defines the operation.

set_repository_id_prefix(val)
Set the naming template for GRAMPS Repository ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as R%d or R%04d.

set_researcher(owner)
Set the information about the owner of the database.

set_save_path(path)
Set the save path for the database.

set_source_id_prefix(val)
Set the naming template for GRAMPS Source ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as S%d or S%04d.

set_undo_callback(callback)
Define the callback function that is called whenever an undo operation is executed.

The callback function receives a single argument that is a text string that defines the operation.

version_supported()
Return True when the file has a supported version.

class gen.db.base.DbWriteBase
Bases: gen.db.base.DbReadBase

GRAMPS database object. This object is a base class for all database interfaces. All methods raise NotImplementedError and must be implemented in the derived class as required.

add_child_to_family(family, child, mrel=<gen.lib.childreftype.ChildRefType object at 0xadb0504>, frel=<gen.lib.childreftype.ChildRefType object at 0xadb052c>, trans=None)
Adds a child to a family.

add_event(event, transaction, set_gid=True)
Add an Event to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_family(family, transaction, set_gid=True)
Add a Family to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_family_event(event, transaction)
Add an Event to the database, assigning internal IDs if they have not already been defined.

add_note(obj, transaction, set_gid=True)
Add a Note to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_object(obj, transaction, set_gid=True)
Add a MediaObject to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_person(person, transaction, set_gid=True)
Add a Person to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_person_event(event, transaction)
Add an Event to the database, assigning internal IDs if they have not already been defined.

add_place(place, transaction, set_gid=True)
Add a Place to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_repository(obj, transaction, set_gid=True)
Add a Repository to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_source(source, transaction, set_gid=True)
Add a Source to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_tag(tag, transaction)
Add a Tag to the database, assigning a handle if it has not already been defined.

add_to_surname_list(person, batch_transaction, name)
Add surname from given person to list of surnames

build_surname_list()
Build the list of locale-sorted surnames contained in the database.

commit_base(obj, data_map, key, transaction, change_time)
Commit the specified object to the database, storing the changes as part of the transaction.

commit_event(event, transaction, change_time=None)
Commit the specified Event to the database, storing the changes as part of the transaction.

commit_family(family, transaction, change_time=None)
Commit the specified Family to the database, storing the changes as part of the transaction.

commit_family_event(event, transaction, change_time=None)
Commit the specified family Event to the database, storing the changes as part of the transaction.

commit_media_object(obj, transaction, change_time=None)
Commit the specified MediaObject to the database, storing the changes as part of the transaction.

commit_note(note, transaction, change_time=None)
Commit the specified Note to the database, storing the changes as part of the transaction.

commit_person(person, transaction, change_time=None)
Commit the specified Person to the database, storing the changes as part of the transaction.

commit_personal_event(event, transaction, change_time=None)
Commit the specified personal Event to the database, storing the changes as part of the transaction.

commit_place(place, transaction, change_time=None)
Commit the specified Place to the database, storing the changes as part of the transaction.

commit_repository(repository, transaction, change_time=None)
Commit the specified Repository to the database, storing the changes as part of the transaction.

commit_source(source, transaction, change_time=None)
Commit the specified Source to the database, storing the changes as part of the transaction.

commit_tag(tag, transaction, change_time=None)
Commit the specified Tag to the database, storing the changes as part of the transaction.

delete_person_from_database(person, trans)
Deletes a person from the database, cleaning up all associated references.

delete_primary_from_reference_map(handle, transaction)
Called each time an object is removed from the database.

This can be used by subclasses to update any additional index tables that might need to be changed.

get_total()
Get the total of primary objects.

get_undodb()
Return the database that keeps track of Undo/Redo operations.

marriage_from_eventref_list(eventref_list)
Get the marriage event from an eventref list.

need_upgrade()
Return True if database needs to be upgraded

rebuild_secondary(callback)
Rebuild secondary indices

reindex_reference_map(callback)
Reindex all primary records in the database.

remove_child_from_family(person_handle, family_handle, trans=None)
Remove a person as a child of the family, deleting the family if it becomes empty.

remove_event(handle, transaction)
Remove the Event specified by the database handle from the database, preserving the change in the passed transaction.

This method must be overridden in the derived class.

remove_family(handle, transaction)
Remove the Family specified by the database handle from the database, preserving the change in the passed transaction.

This method must be overridden in the derived class.

remove_family_relationships(family_handle, trans=None)
Remove a family and its relationships.

remove_from_surname_list(person)
Check whether there are persons with the same surname left in the database.

If not then we need to remove the name from the list. The function must be overridden in the derived class.

remove_note(handle, transaction)
Remove the Note specified by the database handle from the database, preserving the change in the passed transaction.

This method must be overridden in the derived class.

remove_object(handle, transaction)
Remove the MediaObjectPerson specified by the database handle from the database, preserving the change in the passed transaction.

This method must be overridden in the derived class.

remove_parent_from_family(person_handle, family_handle, trans=None)
Remove a person as either the father or mother of a family, deleting the family if it becomes empty.

remove_person(handle, transaction)
Remove the Person specified by the database handle from the database, preserving the change in the passed transaction.

This method must be overridden in the derived class.

remove_place(handle, transaction)
Remove the Place specified by the database handle from the database, preserving the change in the passed transaction.

This method must be overridden in the derived class.

remove_repository(handle, transaction)
Remove the Repository specified by the database handle from the database, preserving the change in the passed transaction.

This method must be overridden in the derived class.

remove_source(handle, transaction)
Remove the Source specified by the database handle from the database, preserving the change in the passed transaction.

This method must be overridden in the derived class.

remove_tag(handle, transaction)
Remove the Tag specified by the database handle from the database, preserving the change in the passed transaction.

This method must be overridden in the derived class.

set_auto_remove()
BSDDB change log settings using new method with renamed attributes

set_birth_death_index(person)
Set the birth and death indices for a person.

set_default_person_handle(handle)
Set the default Person to the passed instance.

set_name_group_mapping(name, group)
Set the default grouping name for a surname.

Needs to be overridden in the derived class.

sort_surname_list()
Sort the list of surnames contained in the database by locale ordering.

transaction_abort(transaction)
Revert the changes made to the database so far during the transaction.

transaction_begin(transaction)
Prepare the database for the start of a new transaction.

Two modes should be provided: transaction.batch=False for ordinary database operations that will be encapsulated in database transactions to make them ACID and that are added to Gramps transactions so that they can be undone. And transaction.batch=True for lengthy database operations, that benefit from a speedup by making them none ACID, and that can’t be undone. The user is warned and is asked for permission before the start of such database operations.

Parameters:	transaction (DbTxn) – Gramps transaction ...
Returns:	Returns the Gramps transaction.
Return type:	DbTxn
transaction_commit(transaction)
Make the changes to the database final and add the content of the transaction to the undo database.

update_reference_map(obj, transaction)
Called each time an object is writen to the database.

This can be used by subclasses to update any additional index tables that might need to be changed.

write_version(name)
Write version number for a newly created DB.

GrampsDbRead
Read classes for the GRAMPS databases.

class gen.db.read.DbBsddbRead
Bases: gen.db.base.DbReadBase, gen.utils.callback.Callback

Read class for the GRAMPS databases. Implements methods necessary to read the various object classes. Currently, there are eight (8) classes:

Person, Family, Event, Place, Source, MediaObject, Repository and Note

For each object class, there are methods to retrieve data in various ways. In the methods described below, <object> can be one of person, family, event, place, source, media_object, respository or note unless otherwise specified.

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
returns a list of handles for the object type, optionally sorted (for Person, Place, Source and Media objects)

iter_<object>_handles()
returns an iterator that yields one object handle per call.

iter_<objects>()
returns an iterator that yields one object per call. The objects available are: people, families, events, places, sources, media_objects, repositories and notes.

get_<object>_event_types()
returns a list of all Event types assocated with instances of <object> in the database.

get_<object>_attribute_types()
returns a list of all Event types assocated with instances of <object> in the database.

close()
Close the specified database.

The method needs to be overridden in the derived class.

db_has_bm_changes()
Return whethere there were bookmark changes during the session.

find_backlink_handles(handle, include_classes=None)
Find all objects that hold a reference to the object handle.

Returns an interator over alist of (class_name, handle) tuples.

Parameters:	
handle (database handle) – handle of the object to search for.
include_classes (list of class names) – list of class names to include in the results. Defaults to None, which includes all classes.
This default implementation does a sequencial scan through all the primary object databases and is very slow. Backends can override this method to provide much faster implementations that make use of additional capabilities of the backend.

Note that this is a generator function, it returns a iterator for use in loops. If you want a list of the results use:

result_list = list(find_backlink_handles(handle))
find_next_event_gramps_id()
Return the next available GRAMPS’ ID for a Event object based off the event ID prefix.

find_next_family_gramps_id()
Return the next available GRAMPS’ ID for a Family object based off the family ID prefix.

find_next_note_gramps_id()
Return the next available GRAMPS’ ID for a Note object based off the note ID prefix.

find_next_object_gramps_id()
Return the next available GRAMPS’ ID for a MediaObject object based off the media object ID prefix.

find_next_person_gramps_id()
Return the next available GRAMPS’ ID for a Person object based off the person ID prefix.

find_next_place_gramps_id()
Return the next available GRAMPS’ ID for a Place object based off the place ID prefix.

find_next_repository_gramps_id()
Return the next available GRAMPS’ ID for a Respository object based off the repository ID prefix.

find_next_source_gramps_id()
Return the next available GRAMPS’ ID for a Source object based off the source ID prefix.

get_bookmarks()
Return the list of Person handles in the bookmarks.

get_child_reference_types()
Return a list of all child reference types assocated with Family instances in the database.

get_dbid()
In BSDDB, we use the file directory name as the unique ID for this database on this computer.

get_dbname()
In BSDDB, the database is in a text file at the path

get_default_handle()
Return the default Person of the database.

get_default_person()
Return the default Person of the database.

get_event_bookmarks()
Return the list of Person handles in the bookmarks.

get_event_from_gramps_id(val)
Find an Event in the database from the passed gramps’ ID.

If no such Family exists, None is returned.

get_event_from_handle(handle)
Find a Event in the database from the passed handle.

If no such Event exists, None is returned.

get_event_handles()
Return a list of database handles, one handle for each Event in the database.

get_event_roles()
Return a list of all custom event role names assocated with Event instances in the database.

get_family_attribute_types()
Return a list of all Attribute types assocated with Family instances in the database.

get_family_bookmarks()
Return the list of Person handles in the bookmarks.

get_family_event_types()
Return a list of all Event types assocated with Family instances in the database.

get_family_from_gramps_id(val)
Find a Family in the database from the passed gramps’ ID.

If no such Family exists, None is return.

get_family_from_handle(handle)
Find a Family in the database from the passed handle.

If no such Family exists, None is returned.

get_family_handles()
Return a list of database handles, one handle for each Family in the database.

get_family_relation_types()
Return a list of all relationship types assocated with Family instances in the database.

get_from_name_and_gramps_id(table_name, gramps_id)
Returns a gen.lib object (or None) given table_name and gramps ID.

Examples:

>>> self.get_from_name_and_gramps_id("Person", "I00002")
>>> self.get_from_name_and_gramps_id("Family", "F056")
>>> self.get_from_name_and_gramps_id("Media", "M00012")
get_from_name_and_handle(table_name, handle)
Returns a gen.lib object (or None) given table_name and handle.

Examples:

>>> self.get_from_name_and_handle("Person", "a7ad62365bc652387008")
>>> self.get_from_name_and_handle("Media", "c3434653675bcd736f23")
get_media_attribute_types()
Return a list of all Attribute types assocated with Media and MediaRef instances in the database.

get_media_bookmarks()
Return the list of Person handles in the bookmarks.

get_media_object_handles(sort_handles=False)
Return a list of database handles, one handle for each MediaObject in the database.

If sort_handles is True, the list is sorted by title.

get_mediapath()
Return the default media path of the database.

get_name_group_keys()
Return the defined names that have been assigned to a default grouping.

get_name_group_mapping(surname)
Return the default grouping name for a surname.

get_name_types()
Return a list of all custom names types assocated with Person instances in the database.

get_note_bookmarks()
Return the list of Note handles in the bookmarks.

get_note_from_gramps_id(val)
Find a Note in the database from the passed gramps’ ID.

If no such Note exists, None is returned.

get_note_from_handle(handle)
Find a Note in the database from the passed handle.

If no such Note exists, None is returned.

get_note_handles()
Return a list of database handles, one handle for each Note in the database.

get_note_types()
Return a list of all custom note types assocated with Note instances in the database.

get_number_of_events()
Return the number of events currently in the database.

get_number_of_families()
Return the number of families currently in the database.

get_number_of_media_objects()
Return the number of media objects currently in the database.

get_number_of_notes()
Return the number of notes currently in the database.

get_number_of_people()
Return the number of people currently in the database.

get_number_of_places()
Return the number of places currently in the database.

get_number_of_repositories()
Return the number of source repositories currently in the database.

get_number_of_sources()
Return the number of sources currently in the database.

get_number_of_tags()
Return the number of tags currently in the database.

get_object_from_gramps_id(val)
Find a MediaObject in the database from the passed gramps’ ID.

If no such MediaObject exists, None is returned.

get_object_from_handle(handle)
Find an Object in the database from the passed handle.

If no such Object exists, None is returned.

get_origin_types()
Return a list of all custom origin types assocated with Person/Surname instances in the database.

get_person_attribute_types()
Return a list of all Attribute types assocated with Person instances in the database.

get_person_event_types()
Return a list of all Event types assocated with Person instances in the database.

get_person_from_gramps_id(val)
Find a Person in the database from the passed gramps’ ID.

If no such Person exists, None is returned.

get_person_from_handle(handle)
Find a Person in the database from the passed handle.

If no such Person exists, None is returned.

get_person_handles(sort_handles=False)
Return a list of database handles, one handle for each Person in the database.

If sort_handles is True, the list is sorted by surnames.

get_place_bookmarks()
Return the list of Person handles in the bookmarks.

get_place_from_gramps_id(val)
Find a Place in the database from the passed gramps’ ID.

If no such Place exists, None is returned.

get_place_from_handle(handle)
Find a Place in the database from the passed handle.

If no such Place exists, None is returned.

get_place_handles(sort_handles=False)
Return a list of database handles, one handle for each Place in the database.

If sort_handles is True, the list is sorted by Place title.

get_repo_bookmarks()
Return the list of Person handles in the bookmarks.

get_repository_from_gramps_id(val)
Find a Repository in the database from the passed gramps’ ID.

If no such Repository exists, None is returned.

get_repository_from_handle(handle)
Find a Repository in the database from the passed handle.

If no such Repository exists, None is returned.

get_repository_handles()
Return a list of database handles, one handle for each Repository in the database.

get_repository_types()
Return a list of all custom repository types assocated with Repository instances in the database.

get_researcher()
Return the Researcher instance, providing information about the owner of the database.

get_save_path()
Return the save path of the file, or “” if one does not exist.

get_source_bookmarks()
Return the list of Person handles in the bookmarks.

get_source_from_gramps_id(val)
Find a Source in the database from the passed gramps’ ID.

If no such Source exists, None is returned.

get_source_from_handle(handle)
Find a Source in the database from the passed handle.

If no such Source exists, None is returned.

get_source_handles(sort_handles=False)
Return a list of database handles, one handle for each Source in the database.

If sort_handles is True, the list is sorted by Source title.
get_source_media_types()
Return a list of all custom source media types assocated with Source instances in the database.

get_surname_list()
Return the list of locale-sorted surnames contained in the database.

get_table_metadata(table_name)
Return the metadata for a valid table name.

get_table_names()
Return a list of valid table names.

get_tag_from_handle(handle)
Find a Tag in the database from the passed handle.

If no such Tag exists, None is returned.

get_tag_from_name(val)
Find a Tag in the database from the passed Tag name.

If no such Tag exists, None is returned.

get_tag_handles(sort_handles=False)
Return a list of database handles, one handle for each Tag in the database.

If sort_handles is True, the list is sorted by Tag name.
get_url_types()
Return a list of all custom names types assocated with Url instances in the database.

has_event_handle(handle)
Return True if the handle exists in the current Event database.

has_family_handle(handle)
Return True if the handle exists in the current Family database.

has_name_group_key(name)
Return if a key exists in the name_group table.

has_note_handle(handle)
Return True if the handle exists in the current Note database.

has_object_handle(handle)
Return True if the handle exists in the current MediaObjectdatabase.

has_person_handle(handle)
Return True if the handle exists in the current Person database.

has_place_handle(handle)
Return True if the handle exists in the current Place database.

has_repository_handle(handle)
Return True if the handle exists in the current Repository database.

has_source_handle(handle)
Return True if the handle exists in the current Source database.

has_tag_handle(handle)
Return True if the handle exists in the current Tag database.

is_open()
Return 1 if the database has been opened.

report_bm_change()
Add 1 to the number of bookmark changes during this session.

request_rebuild()
Notify clients that the data has changed significantly, and that all internal data dependent on the database should be rebuilt.

set_event_id_prefix(val)
Set the naming template for GRAMPS Event ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as E%d or E%04d.

set_family_id_prefix(val)
Set the naming template for GRAMPS Family ID values. The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as F%d or F%04d.

set_mediapath(path)
Set the default media path for database, path should be utf-8.

set_note_id_prefix(val)
Set the naming template for GRAMPS Note ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as N%d or N%04d.

set_object_id_prefix(val)
Set the naming template for GRAMPS MediaObject ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as O%d or O%04d.

set_person_id_prefix(val)
Set the naming template for GRAMPS Person ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as I%d or I%04d.

set_place_id_prefix(val)
Set the naming template for GRAMPS Place ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as P%d or P%04d.

set_redo_callback(callback)
Define the callback function that is called whenever an redo operation is executed.

The callback function receives a single argument that is a text string that defines the operation.

set_repository_id_prefix(val)
Set the naming template for GRAMPS Repository ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as R%d or R%04d.

set_researcher(owner)
Set the information about the owner of the database.

set_save_path(path)
Set the save path for the database.

set_source_id_prefix(val)
Set the naming template for GRAMPS Source ID values.

The string is expected to be in the form of a simple text string, or in a format that contains a C/Python style format string using %d, such as S%d or S%04d.

set_undo_callback(callback)
Define the callback function that is called whenever an undo operation is executed.

The callback function receives a single argument that is a text string that defines the operation.

version_supported()
Return True when the file has a supported version.

gen.db.read.find_surname(key, data)
Creating a surname from raw data of a person, to use for sort and index

gen.db.read.find_surname_name(key, data)
Creating a surname from raw name, to use for sort and index

GrampsDbWrite
Provide the Berkeley DB (DbBsddb) database backend for GRAMPS. This is used since GRAMPS version 3.0

class gen.db.write.BsddbWriteCursor(source, txn=None, **kwargs)
Bases: gen.db.cursor.BsddbBaseCursor

class gen.db.write.DbBsddb
Bases: gen.db.read.DbBsddbRead, gen.db.base.DbWriteBase, gen.updatecallback.UpdateCallback

GRAMPS database write access object.

add_event(event, transaction, set_gid=True)
Add an Event to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_family(family, transaction, set_gid=True)
Add a Family to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_family_event(event, transaction)
Add an Event to the database, assigning internal IDs if they have not already been defined.

add_note(obj, transaction, set_gid=True)
Add a Note to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_object(obj, transaction, set_gid=True)
Add a MediaObject to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_person(person, transaction, set_gid=True)
Add a Person to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_person_event(event, transaction)
Add an Event to the database, assigning internal IDs if they have not already been defined.

add_place(place, transaction, set_gid=True)
Add a Place to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_repository(obj, transaction, set_gid=True)
Add a Repository to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_source(source, transaction, set_gid=True)
Add a Source to the database, assigning internal IDs if they have not already been defined.

If not set_gid, then gramps_id is not set.

add_tag(obj, transaction)
Add a Tag to the database, assigning a handle if it has not already been defined.

add_to_surname_list(person, batch_transaction)
Add surname to surname list

build_surname_list(*args, **kwargs)
Build surname list for use in autocompletion

catch_db_error(func)
Decorator function for catching database errors. If func throws one of the exceptions in DBERRS, the error is logged and a DbError exception is raised.

close(*args, **kwargs)
commit_base(obj, data_map, key, transaction, change_time)
Commit the specified object to the database, storing the changes as part of the transaction.

commit_event(event, transaction, change_time=None)
Commit the specified Event to the database, storing the changes as part of the transaction.

commit_family(family, transaction, change_time=None)
Commit the specified Family to the database, storing the changes as part of the transaction.

commit_family_event(event, transaction, change_time=None)
commit_media_object(obj, transaction, change_time=None)
Commit the specified MediaObject to the database, storing the changes as part of the transaction.

commit_note(note, transaction, change_time=None)
Commit the specified Note to the database, storing the changes as part of the transaction.

commit_person(person, transaction, change_time=None)
Commit the specified Person to the database, storing the changes as part of the transaction.

commit_personal_event(event, transaction, change_time=None)
commit_place(place, transaction, change_time=None)
Commit the specified Place to the database, storing the changes as part of the transaction.

commit_repository(repository, transaction, change_time=None)
Commit the specified Repository to the database, storing the changes as part of the transaction.

commit_source(source, transaction, change_time=None)
Commit the specified Source to the database, storing the changes as part of the transaction.

commit_tag(tag, transaction, change_time=None)
Commit the specified Tag to the database, storing the changes as part of the transaction.

create_id()
delete_primary_from_reference_map(handle, transaction, txn=None)
Remove all references to the primary object from the reference_map.

find_backlink_handles(*args, **kwargs)
Find all objects that hold a reference to the object handle.

Returns an interator over a list of (class_name, handle) tuples.

Parameters:	
handle (database handle) – handle of the object to search for.
include_classes (list of class names) – list of class names to include in the results. Default: None means include all classes.
Note that this is a generator function, it returns a iterator for use in loops. If you want a list of the results use:

result_list = list(find_backlink_handles(handle))
get_cursor(*args, **kwargs)
Helper function to return a cursor over a table

get_dbid()
In BSDDB, we use the file directory name as the unique ID for this database on this computer.

get_default_person(*args, **kwargs)
Return the default Person of the database.

get_from_handle(handle, class_type, data_map)
get_reference_map_cursor(*args, **kwargs)
Returns a reference to a cursor over the reference map

get_reference_map_primary_cursor(*args, **kwargs)
Returns a reference to a cursor over the reference map primary map

get_reference_map_referenced_cursor(*args, **kwargs)
Returns a reference to a cursor over the reference map referenced map

get_undodb()
Return the database that keeps track of Undo/Redo operations.

gramps_upgrade(callback=None)
load(*args, **kwargs)
need_upgrade(*args, **kwargs)
rebuild_secondary(*args, **kwargs)
redo(update_history=True)
reindex_reference_map(*args, **kwargs)
Reindex all primary records in the database.

This will be a slow process for large databases.

remove_event(handle, transaction)
Remove the Event specified by the database handle from the database, preserving the change in the passed transaction.

remove_family(handle, transaction)
Remove the Family specified by the database handle from the database, preserving the change in the passed transaction.

remove_from_surname_list(*args, **kwargs)
Check whether there are persons with the same surname left in the database.

If not then we need to remove the name from the list. The function must be overridden in the derived class.

remove_note(handle, transaction)
Remove the Note specified by the database handle from the database, preserving the change in the passed transaction.

remove_object(handle, transaction)
Remove the MediaObjectPerson specified by the database handle from the database, preserving the change in the passed transaction.

remove_person(handle, transaction)
Remove the Person specified by the database handle from the database, preserving the change in the passed transaction.

remove_place(handle, transaction)
Remove the Place specified by the database handle from the database, preserving the change in the passed transaction.

remove_repository(handle, transaction)
Remove the Repository specified by the database handle from the database, preserving the change in the passed transaction.

remove_source(handle, transaction)
Remove the Source specified by the database handle from the database, preserving the change in the passed transaction.

remove_tag(handle, transaction)
Remove the Tag specified by the database handle from the database, preserving the change in the passed transaction.

set_auto_remove()
BSDDB change log settings using new method with renamed attributes

set_default_person_handle(*args, **kwargs)
Set the default Person to the passed instance.

set_mediapath(path)
Set the default media path for database, path should be utf-8.

set_name_group_mapping(*args, **kwargs)
sort_surname_list()
transaction_abort(transaction)
Revert the changes made to the database so far during the transaction.

transaction_begin(*args, **kwargs)
Prepare the database for the start of a new Transaction.

Supported transaction parameters: no_magic: Boolean, defaults to False, indicating if secondary indices

should be disconnected.
transaction_commit(*args, **kwargs)
Make the changes to the database final and add the content of the transaction to the undo database.

undo(update_history=True)
update_reference_map(obj, transaction, txn=None)
If txn is given, then changes are written right away using txn.

version_supported(*args, **kwargs)
write_version(name)
Write version number for a newly created DB.

class gen.db.write.DbBsddbAssocCursor(source, txn=None, **kwargs)
Bases: gen.db.cursor.BsddbBaseCursor

gen.db.write.clear_lock_file(name)
gen.db.write.find_idmap(key, data)
gen.db.write.find_primary_handle(key, data)
gen.db.write.find_referenced_handle(key, data)
gen.db.write.upgrade_researcher(owner_data)
Upgrade researcher data to include a locality field in the address. This should be called for databases prior to Gramps 3.3.

gen.db.write.write_lock_file(name)
GrampsCursor
class gen.db.cursor.BsddbBaseCursor(txn=None, update=False, commit=False)
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

update(key, data, flags=0, **kwargs)
Write the current key, data pair to the database.

BSDDBtxn
BSDDBTxn class: Wrapper for BSDDB transaction-oriented methods

class gen.db.bsddbtxn.BSDDBTxn(env, db=None)
Bases: object

Wrapper for BSDDB methods that set up and manage transactions. Implements context management functionality allowing constructs like:

with BSDDBTxn(env) as txn:
DB.get(txn=txn) DB.put(txn=txn) DB.delete(txn=txn)
and other transaction-oriented DB access methods, where “env” is a BSDDB DBEnv object and “DB” is a BSDDB database object.

Transactions are automatically begun when the “with” statement is executed and automatically committed when control flows off the end of the “with” statement context, either implicitly by reaching the end of the indentation level or explicity if a “return” statement is encountered or an exception is raised.

abort()
Abort the transaction

begin(*args, **kwargs)
Create and begin a new transaction. A DBTxn object is returned

checkpoint(*args, **kwargs)
Flush the underlying memory pool, write a checkpoint record to the log and then flush the log

commit(flags=0)
End the transaction, committing any changes to the databases

db
delete(key, txn=None, **kwargs)
Removes a key/data pair from the database

discard()
Release all the per-process resources associated with the specified transaction, neither committing nor aborting the transaction

env
get(key, default=None, txn=None, **kwargs)
Returns the data object associated with key

id()
Return the unique transaction id associated with the specified transaction

parent
pget(key, default=None, txn=None, **kwargs)
Returns the primary key, given the secondary one, and associated data

prepare(gid)
Initiate the beginning of a two-phase commit

put(key, data, txn=None, **kwargs)
Stores the key/data pair in the database

recover()
Returns a list of tuples (GID, TXN) of transactions prepared but still unresolved

stat()
Return a dictionary of transaction statistics

txn
GrampsDbTxn
Exports the DbTxn class for managing Gramps transactions and the undo database.

class gen.db.txn.DbTxn(msg, grampsdb, batch=False, **kwargs)
Bases: collections.defaultdict

Define a group of database commits that define a single logical operation.

add(obj_type, trans_type, handle, old_data, new_data)
Add a commit operation to the Transaction.

The obj_type is a constant that indicates what type of PrimaryObject is being added. The handle is the object’s database handle, and the data is the tuple returned by the object’s serialize method.

batch
commitdb
db
first
get_description()
Return the text string that describes the logical operation performed by the Transaction.

get_recnos(reverse=False)
Return a list of record numbers associated with the transaction.

While the list is an arbitrary index of integers, it can be used to indicate record numbers for a database.

get_record(recno)
Return a tuple representing the PrimaryObject type, database handle for the PrimaryObject, and a tuple representing the data created by the object’s serialize method.

last
msg
set_description(msg)
Set the text string that describes the logical operation performed by the Transaction.

timestamp
gen.db.txn.testtxn()
Test suite

GrampsDbUndo
Exports the DbUndo class for managing Gramps transactions undos and redos.

class gen.db.undoredo.DbUndo(grampsdb)
Bases: object

Base class for the gramps undo/redo manager. Needs to be subclassed for use with a real backend.

append(value)
Add a new entry on the end. Needs to be overridden in the derived class.

clear()
Clear the undo/redo list (but not the backing storage)

close()
Close the backing storage. Needs to be overridden in the derived class.

commit(txn, msg)
Commit the transaction to the undo/redo database. “txn” should be an instance of gramps gramps transaction class

db
mapbase
open(value)
Open the backing storage. Needs to be overridden in the derived class.

redo(update_history=True)
Redo a previously committed, then undone, transaction

redo_count
redoq
txn
undo(update_history=True)
Undo a previously committed transaction

undo_count
undo_data(data, handle, db_map, emit, signal_root)
Helper method to undo/redo the changes made

undo_history_timestamp
undo_reference(data, handle, db_map)
Helper method to undo a reference map entry

undodb
undoq
undoredo(func)
Decorator function to wrap undo and redo operations within a bsddb transaction. It also catches bsddb errors and raises an exception as appropriate

class gen.db.undoredo.DbUndoBSDDB(grampsdb, path)
Bases: gen.db.undoredo.DbUndo

Class constructor for gramps undo/redo database using a bsddb recno database as the backing store.

append(value)
Add an entry on the end of the database

close()
Close the undo/redo database

open()
Open the undo/redo database

class gen.db.undoredo.DbUndoList(grampsdb)
Bases: gen.db.undoredo.DbUndo

Implementation of the gramps undo database using a Python list

append(value)
Add an entry on the end of the list

close()
Close the list by resetting it to empty

open()
A list does not need to be opened

gen.db.undoredo.testundo()
DbConst
Declare constants used by database modules

GrampsDbException
Exceptions generated by the Db package.

exception gen.db.exceptions.DbEnvironmentError(msg)
Bases: exceptions.Exception

Error used to report that the database ‘environment’ could not be opened. Most likely, the database was created by a different version of the underlying database engine.

exception gen.db.exceptions.DbException(value)
Bases: exceptions.Exception

exception gen.db.exceptions.DbTransactionCancel(value)
Bases: exceptions.Exception

Error used to indicate that a transaction needs to be canceled, for example becuase it is lengthy and the users requests so.

exception gen.db.exceptions.DbUpgradeRequiredError
Bases: exceptions.Exception

Error used to report that a database needs to be upgraded before it can be used.

exception gen.db.exceptions.DbVersionError
Bases: exceptions.Exception

Error used to report that a file could not be read because it is written in an unsupported version of the file format.

exception gen.db.exceptions.DbWriteFailure(value, value2='')
Bases: exceptions.Exception

Error used to indicate that a write to a database has failed.

messages()
Upgrade utilities
gen.db.upgrade.convert_address(addr)
Convert an address into the new format.

gen.db.upgrade.convert_date_14(date)
gen.db.upgrade.convert_location(loc)
Convert a location into the new format.

gen.db.upgrade.convert_locbase(loc)
Convert location base to include an empty locality field.

gen.db.upgrade.convert_marker(self, marker_field)
Convert a marker into a tag.

gen.db.upgrade.convert_name_14(name)
gen.db.upgrade.convert_name_15(name)
gen.db.upgrade.gramps_upgrade_14(self)
Upgrade database from version 13 to 14.

gen.db.upgrade.gramps_upgrade_15(self)
Upgrade database from version 14 to 15. This upgrade adds: * tagging * surname list * remove marker

gen.db.upgrade.new_attribute_list_14(attribute_list)
gen.db.upgrade.new_child_ref_list_14(child_ref_list)
gen.db.upgrade.new_media_list_14(media_list)
gen.db.upgrade.new_person_ref_list_14(person_ref_list)
gen.db.upgrade.new_source_list_14(source_list)
Backup
Description
This module Provides backup and restore functions for a database. The backup function saves the data into backup files, while the restore function loads the data back into a database.

You should only restore the data into an empty database.

Implementation
Not all of the database tables need to be backed up, since many are automatically generated from the others. The tables that are backed up are the primary tables and the metadata table.

The database consists of a table of “pickled” tuples. Each of the primary tables is “walked”, and the pickled tuple is extracted, and written to the backup file.

Restoring the data is just as simple. The backup file is parsed an entry at a time, and inserted into the associated database table. The derived tables are built automatically as the items are entered into db.

gen.db.backup.backup(database)
Exports the database to a set of backup files. These files consist of the pickled database tables, one file for each table.

The heavy lifting is done by the private __do__export function. The purpose of this function is to catch any exceptions that occur.

@param database: database instance to backup @type database: DbDir

gen.db.backup.restore(database)
Restores the database to a set of backup files. These files consist of the pickled database tables, one file for each table.

The heavy lifting is done by the private __do__restore function. The purpose of this function is to catch any exceptions that occur.

@param database: database instance to restore @type database: DbDir