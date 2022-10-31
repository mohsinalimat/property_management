# Copyright (c) 2022, Nihantra C. Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Tenancy(Document):
	pass

def tenant_schedule(doc, event):
    for d in doc.get('tenant_schedule'):
        if d.schedule_date:
            event = frappe.db.get_list('Event',filters={'tenant_schedule_id': d.tenant_schedule_id},fields=['tenant_schedule_id'],as_list=True)
            if not event:
                new_event = frappe.get_doc(dict(
                    doctype = 'Event',
                    starts_on = d.schedule_date,
                    subject = doc.asset_name +' - '+ d.schedule_date,
                    asset_id = doc.asset,
                    tenant_schedule_id = d.tenant_schedule_id
                ))
                new_event.append('event_participants', {
                    'reference_doctype': "Asset", 'reference_docname': doc.asset
                    })
                new_event.append('event_participants', {
                    'reference_doctype': "Tenancy", 'reference_docname': doc.name
                    })
                new_event.save()