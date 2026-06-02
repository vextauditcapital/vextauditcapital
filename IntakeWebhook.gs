// ============================================================
// VEXT AUDIT CAPITAL — GOOGLE APPS SCRIPT WEBHOOK DISPATCHER
// File: IntakeWebhook.gs
// ============================================================

/**
 * Handles incoming Web3Forms submissions and routes them to existing Vext core agents.
 * 
 * @param {Object} rawData - Parsed JSON object from the Web3Forms webhook.
 * @return {ContentOutput} - Apps Script TextOutput containing status response.
 */
function handleWeb3FormsWebhook(rawData) {
  try {
    Logger.log("Web3Forms Webhook triggered.");
    
    // Helper function to extract either flat or nested values (handles Web3Forms wrappers)
    function getVal(key) {
      if (rawData[key] !== undefined) return rawData[key];
      if (rawData.data && rawData.data[key] !== undefined) return rawData.data[key];
      if (rawData.params && rawData.params[key] !== undefined) return rawData.params[key];
      return "";
    }

    // Parse children array robustly
    var childrenParsed = [];
    try {
      var rawChildren = getVal("children");
      if (rawChildren) {
        if (typeof rawChildren === "string") {
          childrenParsed = JSON.parse(rawChildren);
        } else {
          childrenParsed = rawChildren;
        }
      }
    } catch(e) {
      Logger.log("Error parsing children details: " + e.message);
    }

    // Extract core fields
    var subject = getVal("subject") || "";
    var name = getVal("name");
    var email = getVal("email");
    var comments = getVal("comments") || getVal("message") || getVal("msg");
    var service = getVal("service") || getVal("svc");
    var amount = getVal("amount") || getVal("amt");
    var designation = getVal("designation") || getVal("desig");
    var phone = getVal("phone");
    var company = getVal("company");
    var country = getVal("country");
    var gstin = getVal("gstin") || getVal("gst");
    var industry = getVal("industry");
    var source = getVal("source") || "Onboard Page";
    
    // Extract relationship profiling fields
    var birthday = getVal("birthday") || getVal("bday");
    var anniversary = getVal("anniversary") || getVal("anni");
    var spouseName = getVal("spouse_name") || getVal("spouse");
    var spouseBirthday = getVal("spouse_birthday") || getVal("sbday");
    var fatherName = getVal("father_name") || getVal("father");
    var fatherBirthday = getVal("father_birthday") || getVal("fbday");
    var motherName = getVal("mother_name") || getVal("mother");
    var motherBirthday = getVal("mother_birthday") || getVal("mbday");

    // Normalize data into a single standard payload format
    // Containing BOTH flat and nested keys to fully satisfy existing agents (A1, A3, A5 etc.)
    var normalizedData = {
      name: name,
      fullName: name,
      email: email,
      phone: phone,
      company: company,
      country: country,
      gst: gstin,
      gstin: gstin,
      industry: industry,
      source: source,
      svc: service,
      service: service,
      amt: amount,
      amount: amount,
      msg: comments,
      message: comments,
      dpdp_consent: "yes", // Submitting client intake form automatically grants relationship consent
      bday: birthday,
      birthday: birthday,
      anni: anniversary,
      anniversary: anniversary,
      spouse: spouseName,
      spouse_name: spouseName,
      sbday: spouseBirthday,
      spouse_birthday: spouseBirthday,
      father: fatherName,
      father_name: fatherName,
      fbday: fatherBirthday,
      father_birthday: fatherBirthday,
      mother: motherName,
      mother_name: motherName,
      mbday: motherBirthday,
      mother_birthday: motherBirthday,
      children: childrenParsed
    };

    // Routing Logic:
    // If the submission is a detailed client intake from onboard.html (marked by NEW CLIENT INTAKE in subject,
    // or has relationship keys populated like birthday/anniversary, or has active svc/amt), route to Onboard Intake.
    var isClientIntake = (subject.indexOf("NEW CLIENT INTAKE") !== -1) || 
                         (source && source.toLowerCase().indexOf("onboard") !== -1) ||
                         (birthday || anniversary || service);

    if (isClientIntake) {
      Logger.log("Routing Web3Forms submission to handleOnboardIntake for client: " + email);
      handleOnboardIntake(normalizedData);
    } else {
      Logger.log("Routing Web3Forms submission to handleContactFormSubmission for lead: " + email);
      handleContactFormSubmission(normalizedData);
    }

    return ContentService.createTextOutput(JSON.stringify({ 
      "status": "success", 
      "message": "Logged successfully via Web3Forms Router",
      "routed_to": isClientIntake ? "handleOnboardIntake" : "handleContactFormSubmission"
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    Logger.log("Error in handleWeb3FormsWebhook: " + error.toString());
    return ContentService.createTextOutput(JSON.stringify({ 
      "status": "error", 
      "message": error.toString() 
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
