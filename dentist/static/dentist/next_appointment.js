document.addEventListener('DOMContentLoaded', function(){

    //
    
    //



    document.addEventListener('click', event=>{
        const element = event.target;
        if(element.className === 'edit'){
            //change the title to save
            const id = element.id;
            console.log(id);
            window.open(`/change_appointment/${id}`, "_blank", "top=100,left=200,height=400, width=900")   
            element.innerHTML = 'تعديل الموعد';
            const parent = element.parentElement;
            const grandparent = parent.parentElement;
            console.log(grandparent);
            const item = grandparent.children[2];
            console.log(item);

        }
    })
    //archive appointment//
    document.addEventListener('click', event=>{
        const atom = event.target;
        if(atom.id === 'archive'){
            // console.log(patient_name)
            const parent = atom.parentElement;
            const grandparent = parent.parentElement;
            const notes = document.querySelector('#notes');
            const patient_name = document.querySelector('#patient_name');
            // const treatment = document.querySelector('#treatment')
            const paid = document.querySelector('#paid_amount')
            const name = grandparent.children[0].innerHTML;
            const treatment_type = document.querySelector('#treatment_type');
            treatment_type.value = grandparent.children[1].innerHTML;
            notes.value = grandparent.children[3].innerHTML;
            patient_name.value = name;
            
           
            
            //console.log('dddd');
            document.querySelector('#new_appointment').style.display = 'block';
            document.querySelector('#resechedule-form').style.display = 'none';
            const id = parent.children[0].id;
            patient_name.dataset.id = id;
            console.log(id);
            

            


            



        }
        
    })
   
});
function show_schedule_form(){
    document.querySelector('#new_appointment').style.display = 'none';
    document.querySelector('#resechedule-form').style.display = 'block';
}

function update_schedule(){
    const patient_name = document.querySelector('#patient_name');
    const treatment = document.querySelector('#treatment_type').value;
    const paid_amount = document.querySelector('#paid_amount').value;
    const date = document.querySelector('#new_date').value;
    const notes = document.querySelector('#notes').value;
    const id = patient_name.dataset.id;
    const data = {'id': id,'name': patient_name, 'treatment': treatment, 'paid_amount': paid_amount, 'date': date, 'notes': notes}
    console.log(data);
    fetch('update_schedule',{
        method: 'POST',
        headers: {
            'Content-TYPE' : 'application/json',
        },
        body: JSON.stringify(data), 

    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
    })
}
function archived(){
    const patient_name = document.querySelector('#patient_name');
    const treatment = document.querySelector('#treatment_type').value;
    const id = patient_name.dataset.id;
    console.log(id); 
    const archive_data = {'id': id, 'treatment_type': treatment}
    fetch('archived', {
        method: 'POST',
        headers: {
            'Content-TYPE' : 'application/json',
        },
        body : JSON.stringify(archive_data),
        
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
    })
    window.location.reload();
}
