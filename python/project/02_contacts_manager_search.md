# Project 02: Contacts Manager with Search

## Estimated Time
3 to 5 hours

## Goal
Create a CLI contacts manager to add, update, delete, search, and persist contacts.

## Functional Requirements
- Add contact:
  - name
  - phone
  - email
  - tags (comma-separated)
- List all contacts.
- Update contact by ID.
- Delete contact by ID.
- Search contacts by:
  - name substring
  - phone exact
  - tag
- Save/load contacts in JSON.

## Non-Functional Requirements
- Validate email and phone format (basic checks).
- No duplicate phone numbers.

## Input/Output Shape
- Contact dictionary:
```python
{
  "id": 3,
  "name": "Aman",
  "phone": "9876543210",
  "email": "aman@mail.com",
  "tags": ["friend", "work"]
}
```

## Concepts Practiced
- `list` of contacts
- `dict` records
- `set` for duplicate phone check
- string search and normalization (`lower()`)

## HLD
- `main.py`: menu
- `contacts.py`: operations
- `validators.py`: phone/email checks
- `storage.py`: JSON persistence

## LLD
- `validate_phone(phone) -> bool`
- `validate_email(email) -> bool`
- `add_contact(contacts, contact) -> (ok, msg)`
- `update_contact(contacts, contact_id, updates) -> bool`
- `delete_contact(contacts, contact_id) -> bool`
- `search_by_name(contacts, text) -> list[dict]`
- `search_by_phone(contacts, phone) -> list[dict]`
- `search_by_tag(contacts, tag) -> list[dict]`
- `load_contacts(path) -> list[dict]`
- `save_contacts(path, contacts) -> None`

## Passing Criteria
- Duplicate phone add is rejected.
- Search works for partial name.
- Update persists after restart.
- Delete removes correct entry.

## Implementation Roadmap
1. Build contact model structure and storage.
2. Build add/list features.
3. Build update/delete.
4. Build 3 search modes.
5. Add validations and friendly errors.

## Optional Extensions
- Import/export CSV.
- Favorites list.
