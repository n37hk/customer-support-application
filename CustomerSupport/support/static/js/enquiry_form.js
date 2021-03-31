function validateForm(){
    if(($("#name").val().trim() === "") ||
    ($("#email").val().trim() === "") ||
    ($("#phone").val().trim() === "") ||
    ($("#query").val().trim() === "")){
        alert("Please fill in all the fields.");
        return false;
    }else if(!$.isNumeric($("#phone").val().trim()) || ($("#phone").val().trim().length < 10)){
        alert("Phone number is invalid");
        return false;
    }else if($("#query").val().trim().split(" ").length > 30){
        alert("Please limit your query to maximum 30 words");
        return false;
    }else{
        return true;
    }
}