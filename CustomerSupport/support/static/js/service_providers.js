function deleteEntry(id){
    $.ajax({
        url: "/support/service-providers/remove",
        type: "DELETE",
        data: {
            id: id
        },
        success: function(response){
            location.assign('/support/service-providers');
        },
        error: function(jqXHR){}
    })
}