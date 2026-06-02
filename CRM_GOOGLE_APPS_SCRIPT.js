/**
 * Vext Audit Capital - CRM Sheets Onboarding Logging Apps Script
 *
 * INSTRUCTIONS FOR DEPLOYMENT:
 * 1. Open your master Google Sheet (ID: 1Xj2RaD-TuP8ieDn8JKhy77alYKYWTM4S3ejnVTL8Q1k) or your active CRM Sheet.
 * 2. Click on Extensions -> Apps Script.
 * 3. Delete any default code and paste this script.
 * 4. Click the Save icon (floppy disk).
 * 5. Click "Deploy" -> "New deployment".
 * 6. Select Type: "Web app".
 * 7. Configure:
 *    - Description: Vext Onboarding Webhook
 *    - Execute as: "Me" (your account)
 *    - Who has access: "Anyone" (crucial for Web3Forms to access it)
 * 8. Click "Deploy", authorize permissions, and copy the "Web app URL".
 * 9. Go to your Web3Forms dashboard (web3forms.com), navigate to your Access Key settings, 
 *    enable Webhooks, paste this URL, and save.
 */

function doPost(e) {
  try {
    var response = HtmlService.createHtmlOutput();
    
    // Parse incoming payload (handles url-encoded and raw json bodies)
    var data;
    if (e.postData.type === "application/json") {
      data = JSON.parse(e.postData.contents);
    } else {
      data = e.parameter;
    }
    
    // Web3Forms can wrap form fields in a nested object (e.g., "data" or "params")
    // This helper extracts either flat or nested values
    function getVal(key) {
      if (data[key] !== undefined) return data[key];
      if (data.data && data.data[key] !== undefined) return data.data[key];
      if (data.params && data.params[key] !== undefined) return data.params[key];
      return "";
    }
    
    // Map webhook payload properties to column headers
    var timestamp = new Date();
    var service = getVal("service") || getVal("svc");
    var amount = getVal("amount") || getVal("amt");
    var currency = getVal("currency") || getVal("cur") || "INR";
    var name = getVal("name");
    var designation = getVal("designation") || getVal("desig");
    var email = getVal("email");
    var phone = getVal("phone");
    var company = getVal("company");
    var country = getVal("country");
    var gstin = getVal("gstin") || getVal("gst");
    var industry = getVal("industry");
    var source = getVal("source");
    var comments = getVal("comments") || getVal("comments") || getVal("message");
    
    // Relationship profile fields
    var birthday = getVal("birthday") || getVal("bday");
    var anniversary = getVal("anniversary") || getVal("anni");
    var spouseName = getVal("spouse_name") || getVal("spouse");
    var spouseBirthday = getVal("spouse_birthday") || getVal("sbday");
    var fatherName = getVal("father_name") || getVal("father");
    var fatherBirthday = getVal("father_birthday") || getVal("fbday");
    var motherName = getVal("mother_name") || getVal("mother");
    var motherBirthday = getVal("mother_birthday") || getVal("mbday");
    var children = getVal("children");
    
    // Access target sheet and set up headers if sheet is empty
    var sheet;
    try {
      // Direct integration with VAC 360-Degree master sheet: 1Xj2RaD-TuP8ieDn8JKhy77alYKYWTM4S3ejnVTL8Q1k
      sheet = SpreadsheetApp.openById("1Xj2RaD-TuP8ieDn8JKhy77alYKYWTM4S3ejnVTL8Q1k").getActiveSheet();
    } catch(err) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    }
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        "Timestamp", "Service", "Amount", "Currency", "Client Name", 
        "Designation", "Email", "Phone", "Company", "Country", 
        "GSTIN", "Industry", "Referral Source", "Comments / Message",
        "Birthday", "Anniversary", "Spouse Name", "Spouse Birthday",
        "Father Name", "Father Birthday", "Mother Name", "Mother Birthday", "Children Details"
      ]);
      // Format headers
      var headerRange = sheet.getRange(1, 1, 1, 23);
      headerRange.setFontWeight("bold");
      headerRange.setBackground("#1D0404");
      headerRange.setFontColor("#C5A059");
    }
    
    // Append the row of new data
    sheet.appendRow([
      timestamp, service, amount, currency, name,
      designation, email, phone, company, country,
      gstin, industry, source, comments,
      birthday, anniversary, spouseName, spouseBirthday,
      fatherName, fatherBirthday, motherName, motherBirthday, children
    ]);
    
    // Sort so latest always appears at the top (under headers)
    if (sheet.getLastRow() > 2) {
      var dataRange = sheet.getRange(2, 1, sheet.getLastRow() - 1, 23);
      dataRange.sort({ column: 1, ascending: false });
    }
    
    return ContentService.createTextOutput(JSON.stringify({ "status": "success", "message": "Logged successfully" }))
                         .setMimeType(ContentService.MimeType.JSON);
                         
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ "status": "error", "message": error.toString() }))
                         .setMimeType(ContentService.MimeType.JSON);
  }
}
