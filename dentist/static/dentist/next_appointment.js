document.addEventListener('DOMContentLoaded', function(){
    document.addEventListener('click', event=>{
        const element = event.target;
        if(element.className === 'edit'){
            //change the title to save
            const id = element.id;
            console.log(id);
            window.open(`/modify_appointment/${id}`, "_blank", "top=100,left=200,height=400, width=900")   
            element.innerHTML = 'save';
            const parent = element.parentElement;
            const grandparent = parent.parentElement;
            console.log(grandparent);
            const item = grandparent.children[2];
            console.log(item);

        }
    })
    
    document.addEventListener('click', event=>{
        const item = event.target;
        if(item.className === 'remove'){
            const parentitem = item.parentElement;
            const granditem = parentitem.parentElement;
            console.log(granditem);
            
            granditem.remove();
        }

        //
    });
});
