
// function deleteNote(noteId){
//     //this will take the noteId, send post request to del note endpoint
//     fetch('/delete-note',{
//         method: 'DELETE',
//         body: JSON.stringify({ noteId: noteId})
//     }).then((_res) =>{
//         //and then reload window nd redirect to home page
//         $(`.{noteId}`).remove();
//         // window.location.href = '/';
//     })
// }
const deleteNote = id=> fetch(`/delete-note`,{
    method: 'DELETE',
    body: JSON.stringify({ noteId: id})
}).then((_res) =>{
    //and then reload window nd redirect to home page
    // let x = activity_id +  1;
    $(`.${id}`).remove();
    // document.getElementById('{{note.id}}').style.display = 'none';  
    
    $(`#app-${id}`).remove();
    alert("deleted " + id)
})
// const deleteNote = id => fetch(`/delete-note/${id}`,{
//     method: 'DELETE',
//     body: JSON.stringify({ activity_id: id})
// }).then((_res) =>{
//     //and then reload window nd redirect to home page
//     // let x = activity_id +  1;
//     $(`#act-${id}`).remove();
//     alert("deleted " + id)
// }) 
let onAddNote = () =>{
    document.getElementById('onAddNote').style.display = 'block';  
    document.getElementById('notes').style.display = 'none';  
}
// let arrayOfNotes = []

// 'clickedNote({{ note.title, note.data }})
// document.getElementById("app").addEventListener("click", function() {
//     document.getElementById("noteData").innerHTML = this.data;
//     // document.getElementById('notes').style.display = 'block';
//   });