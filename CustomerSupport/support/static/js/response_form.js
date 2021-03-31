function validateForm(){
    if($("#response").val().trim() === ""){
        alert("Please fill the response field");
        return false;
    }else if($("#response").val().trim().split(" ").length > 30){
        alert("Please limit your response to maximum 30 words");
        return false;
    }else{
        return true;
    }
}