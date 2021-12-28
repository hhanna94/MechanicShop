
$(document).ready(
    function () {
        //Create a variable for the CarQuery object.  You can call it whatever you like.
        var carquery = new CarQuery();

        //Run the carquery init function to get things started:
        carquery.init();

        //Optionally, you can pre-select a vehicle by passing year / make / model / trim to the init function:
        //carquery.init('2000', 'dodge', 'Viper', 11636);

        //Optional: Pass sold_in_us:true to the setFilters method to show only US models. 
        carquery.setFilters({ sold_in_us: true });

        //Optional: initialize the year, make, model, and trim drop downs by providing their element IDs
        carquery.initYearMakeModelTrim('car-years', 'car-makes', 'car-models', 'car-model-trims');

        //Optional: set the onclick event for a button to show car data.
        $('#cq-show-data').click(function () { carquery.populateCarData('car-model-data'); });

});

function getCarData(model_num) {
    $.getJSON("https://www.carqueryapi.com/api/0.3/?callback=?", {cmd:"getModel", model:model_num}, function(data) {
        console.log(data)
        let result = data[0]

        let setEngineLocation = document.querySelector("#engine_location")
        let setEngineType = document.querySelector("#engine_type")
        let setCylinders = document.querySelector("#cylinders")
        let setDrive = document.querySelector("#drive")
        let setTransmission = document.querySelector("#transmission")
        let setTrim = document.querySelector("#trim")

        result.model_engine_position ?  setEngineLocation.innerText = result.model_engine_position : setEngineLocation.innerHTML = "<em>Data not available</em>"
        result.model_engine_type ?  setEngineType.innerText = result.model_engine_type  : setEngineType.innerHTML = "<em>Data not available</em>"
        result.model_engine_cyl ? setCylinders.innerText = result.model_engine_cyl : setCylinders.innerHTML = "<em>Data not available</em>"
        result.model_drive ? setDrive.innerText = result.model_drive : setDrive.innerHTML = "<em>Data not available</em>"
        result.model_transmission_type ? setTransmission.innerText = result.model_transmission_type : setTransmission.innerHTML = "<em>Data not available</em>"
        result.model_trim ?  setTrim.innerText = result.model_trim : setTrim.innerHTML = "<em>Data not available</em>"
    })
}

function displayNotes() {
    document.querySelector("#previous_notes").classList.remove("hide")
    document.querySelector("#view_notes_button").classList.add("hide")
}

function hideNotes() {
    document.querySelector("#view_notes_button").classList.remove("hide")
    document.querySelector("#previous_notes").classList.add("hide")
}

function editCustomer() {
    document.querySelector("#edit_customer").classList.remove("hide")
    document.querySelector("#customer_details").classList.add("hide")
}

function editService() {
    document.querySelector("#edit_service_form").classList.remove("hide")
    document.querySelector("#service_details").classList.add("hide")
}