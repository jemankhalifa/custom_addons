<p align="right">
  <img src="static/description/company_logo.jpeg" alt="Net4X Innovation" width="150"/>
</p>


# Check Printing Management


Description
===========
Manage check payments

Installation
============
1. Copy the module folder to your Odoo addons directory.
2. Restart the Odoo server.
3. Go to the Odoo Apps menu and click "Update Apps List".
4. Search for **"Manage check payments"** and click "Install".

Configuration
=============
After installation:
    1. Go to **Accounting->Vendors->Check Layout** to configure the module.
    2. Set up **X,Y Paddings for each Field** as needed.

Usage
=====

Enable Check Printing Settings
-----------------------------
    1. Go to **Apps > Accounting**.
    2. Click on **Settings**.
    3. Look for the **Check Printing** option and ensure it is enabled.
    4. Save the settings by clicking **Save**.

Create a New Check
------------------
    1. Navigate to **Accounting > Payments**.
    2. Click the **Create** button to create a new payment.
    3. Enter the following details:
       - **Vendor/Customer**.
       - **Amount**.
       - **Payment Method**: Select **Check**.
       - **Bank Account**.
       - **Payment Date**.
    4. Click **Save**.

Print the Check
---------------
    1. After saving the check, you will find a **Print Check** button.
    2. Click the button to open the print template selection window.
    3. Choose the appropriate check format based on the bank you are dealing with.
    4. Click **Print**.
    5. The check will be sent to your printer for printing.

Update the Check Status
-----------------------
    - Once the check is printed, its status in the system will be updated to **Printed**.
    - After the check is cashed, you can update its status to **Paid**.
    - If the check is canceled, you can change its status to **Cancelled**.


Credits
=======
- Developed by **Net4x Innovation**.

License
=======
This module is **proprietary** and licensed under the **Odoo Proprietary License v1.0 (OPL-1.0)**.
Redistribution, modification, or resale is **not permitted** without prior authorization from the copyright holder.

For full license terms, see the `LICENSE` file or visit:
https://www.odoo.com/documentation/user/18.0/legal/licenses/licenses.html


Support
=======

**Net4X Innovation**  
🌐 [https://net4x-innovation.com](https://net4x-innovation.com/contactus)