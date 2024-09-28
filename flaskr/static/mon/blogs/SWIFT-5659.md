1Ticket: https://mpowermsl.atlassian.net/browse/SWIFT-5659

Branch: [micropoweraus / swiftpos.v10 / Branch feature/s.fernandez/SWIFT-5659-6.1-import-multiple-host-file — Bitbucket](https://bitbucket.org/micropoweraus/swiftpos.v10/branch/feature/s.fernandez/SWIFT-5659-6.1-import-multiple-host-file?dest=develop)

SoW [Metcash Platinum Host - Scope of Works 240723.docx](https://ooliogroup.sharepoint.com/:w:/r/sites/swiftpos/RD/Scope%20of%20Works/Metcash%20Platinum%20Host%20-%20Scope%20of%20Works%20240723.docx?d=wd30e2dba588c8e1548ed3d98722c5313&csf=1&web=1&e=q4v0y0 "https://ooliogroup.sharepoint.com/:w:/r/sites/swiftpos/RD/Scope%20of%20Works/Metcash%20Platinum%20Host%20-%20Scope%20of%20Works%20240723.docx?d=wd30e2dba588c8e1548ed3d98722c5313&csf=1&web=1&e=q4v0y0")

# Notes
#### TODO
##### Issues:
- Getting error in `GetValidPriceLevels` when `ImportPromoLocations` is -1.
- 

##### Changes Made:
- ~~Rename Customer Ids to Hosts, set as read-only, change the display value to "\<customer id\> - \<host name\>"~~
- ~~Add to new text boxes: Customer ID and Host name.~~
- ~~Add a "New" button for adding Customer Id.~~
- ~~Rename Location List to Location Cost List, change to multi select, and move it under the Supplier.~~
- ~~Move Invoices Only to the top. If ticked, disable the fields that are used in Host Import.~~
- ~~Set Preferred Supplier Validation: ~~
	- ~~If ticked:~~
		- ~~Check if there's already a preferred Supplier. ~~
		- ~~Prompt to confirm the selection of new preferred Supplier.~~
		- ~~Clear Location Cost List value of the previous preferred Supplier.~~
		- ~~Enable Location Cost List and require it to be set.~~
	- ~~If unticked, disabled and clear the Location Cost List.~~
- ~~Import Promo Locations should be unique between Customer Ids. ???~~
- ~~Change the Display Value of Customer Ids to  "\<customer id\> - \<host name\>" in Metcash Import and Import Invoices.~~
- ~~Remove Supplier Custom Search that is opening after Importing Invoices and use the Supplier set in Metcash Customer Settings.~~
- ~~Invoice Locations should be able to select multiple locations and allow select none.~~

- Create Metcash Customer Settings.
- Allow a Customer ID level configuration for Host Files, instead of Location Group. 
- Hard coded 'Metcash' Supplier can be found in [`ImportSuppliers`](import-suppliers.md), [`createSpProduct`](create-spproduct.md) and [`GetPMSUpdateScript`](import-supplier-get-pms-update-script.md).
- Made New Product enabled by default.
- Import Promotions Locations should be **Multi Select**.
- Set 'Import New Products as Active' and 'Update Stock Size' to True(Read only and not visible).
- Set 'Export URL' to Empty(Read only and not visible).
- Add  [[metcash-customer-settings-table]] in Database Upgrade.
- Add Promotion Group and Locations in `MCPromotionTable`.

#### How to test it
- Configure Metcash Customer Settings.
- Go to BO > Data Export > Data Portal > Metcash / ALM & IBA and do an Import.
	- Select a Customer Id from the Combo box.
	- You don't have to set the Price Level because it's already configured in the Customer Settings
- After doing an Import, go to Product Records > Select a Product > Edit:
	- Check if the Price has been updated for the selected Price Level.
	- Click the Supplier Button and check if the selected Supplier is added.
- Go to Product Records > Specials/Promotions and check if the selected Import Promo Locations is set.

### ~~Global Settings Section~~ 
![[SWIFT-5659-image.png]]

Keep this section, but make the following changes… 

- ==“Update Stock Size” – remove.== Should always be “yes” and NOT visible. 
- ==Remove “Export URL”==
- ==“Import New Products as active” – Should always be “yes” and NOT visible== - if it's being imported  from "Match Products" then the intention is to sell it. 


### ~~Location Group (Venue) Settings~~ 
![[Pasted image 20240809105900.png]]

- ==REMOVE SECTION! ==
- ==To be replaced with “Metcash Customer Settings”== 


![[Pasted image 20240809124056.png]]
### In The Data Portal, “Metcash/ALM”, Import screen… 
Select files to collect and process. 
For the selected files, download all currently available. 

- Screen to ==show available “Customer Codes”== (instead of current behavior: Location Groups). 
Download files for one Customer Code at a time. 
- Show customer code associated to their store – what does this mean? 
- Do we still need Price Level selection on the “Import” screen? 
- When selecting new files, should we force to download all up to the select file (ie. need to import earlier files). If reprocessing a file, and all previous files have already been processed, then allow selection of that one file only. 
	SwiftPOS downloads and processes the file in the one action. Therefore, the operator can select the Host Files they wish to download/process. ie. so a particular store can be downloaded/processed at a later time.

# Related Chat

#### Rob Coleman 
hmmm, brain is hurting thinking about this.

each B2B account needs to be assigned to a supplier, in the old days (the way it used to work) there was only one B2B account and it would be assigned to a hard coded supplier called "Metcash" ( 1 to 1 relationship) now we can have many B2B accounts and choose which supplier they get mapped to. The set preferred is a bit odd, might leave that one for now as I'm not 100% sure it will work. 

Import promotion locations will be used when creating the promotion for M&M rules as per image:

and ordinary promotions

The promotion group is also used here in an ordinary  promotion.

Not sure what the member promotion group is, might need to reach out to Brad or see if he has notes about it in the tickets.

Invoice Locations ( I think ) will be used when importing invoices, however previously it was the locations in a location group, but now I think you will ==select one of the new suppliers associated to the B2B account and that then populates the locations the invoices can be imported into.== - check with Brad on that, the memory is a little fuzzy. Also check the purpose of Invoices only, it might be for sites not importing host, but only invoices.