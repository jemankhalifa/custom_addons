ZOHO BOOKS INTEGRATION
-----------------------------
1.creat Zoho account
2.create a webhook in :https://books.zoho.com/app/885236920#/settings/automation/actions/webhooks/
That contains the following structure:
	1.NAME:odoo customers webhook (or any other name of your choice)
	2.MODULE:Customers 
	1.URL TO NOTIFY:(the domain of your server)/zoho/books 
	2.Authorization Type:Self Authorization 
	3.Body:form-data 
		contact_name:${CONTACT.CONTACT_NAME}
		contact_id:${CONTACT.CONTACT_ID}1000
2.create a webhook in :https://books.zoho.com/app/885236920#/settings/automation/actions/workflows/ 
That contains the following structure:
	1.NAME:odoo customers rule (or any other name of your choice)
	2.MODULE:Customers 
	3.WORKFLOW TYPE:Event Based
	4.ACTION TYPE:Event Based
	2.Execute the workflow when:Any field is updated( or any Triger of your choice for integration resons)
	3.Execute when the record is: Edited each time
	* You may configure a criteria for the record included in the sync process(for example  select to sync only the customers with active status only), with immediate or time based action(depnding on your desier of repeating the sync for the integration process)	
	* You may configure a failuer notification va (Email Alerts,Wbhooks or a Custom Functions)	
-----------------------------
If you choose two way integration(also sync odoo updates with zoho) you must create a client account in Zoho API Consolle in :https://api-console.zoho.com/ withe the type Server-based Applications That contains the following structure:
	1.Client Name : Odoo Books API (or any other name of your choice)
	2.Homepage URL  :(the domain of your server)/zoho
	1.Authorized Redirect URIs  :(the domain of your server)/zoho/oauth2/callback
Thin you should take the value of Client ID  and Client Secret and add them in your odoo company profile under Zoho Information Tab
-----------------------------
