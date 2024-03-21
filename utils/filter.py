from typing import List
from models.contact import Contact

def search_filter(contacts: List[Contact], q: str=None) -> List[Contact]:
    """returns a list of contacts filtered."""
    if not q:
        return contacts
    res = []
    for c in contacts:
        if q in c.first_name or q in c.last_name or q in c.email:
            res.append(c)
    return res

def sort(contacts: List[Contact], field: str=None, reverse: bool=False) -> List[Contact]:
    """returns a list of contacts sorted."""
    if not field or not hasattr(Contact, field):
        field = "id"
    return sorted(contacts, key=lambda x: x.__getattribute__(field), reverse=reverse)