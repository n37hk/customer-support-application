function validateForm(){
    if(!$("#reviewSatisfied").is(":checked") && !$("#reviewUnsatisfied").is(":checked")){
        alert("Please select one of the options");
        return false;
    }else{
        return true;
    }
}