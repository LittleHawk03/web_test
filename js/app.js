const tableElement= document.querySelector(".datas")
function render(){
    fetch('http://localhost:3000/')
    // .then(response => {
    //   //handle response            
    //   console.log(response.json());
    // })
    .then(data => {
      let rows = '';
      data.todos.forEach(todo => {
        rows += `
          <tr class="datas">
            <td class="stt">${todo['STT']}</td>
            <td class="name">${todo['fullname']}</td>
            <td class="Username">${todo['Username']}</td>
            <td class="year">${todo['year of birth']}</td>
            <td class="gender">${todo['gender']}</td>
            <td class="university">${todo['university']}</td>
            <td class="field">${todo['field']}</td>
            <td class="delete"><a href="./remove?_id=${todo['_id']}">🗑️</a></td>
            <td class="update"><a href="./update?_id=${todo['_id']}">📝</a></td>
          </tr>
        `;
      });
  
      // set the HTML content of the table
      table.innerHTML = `
        <tr id="row">
          <th class="stt">stt</th>
          <th class="name">Name of candidate</th>
          <th class="Username">Username</th>
          <th class="year">Year of Birth</th>
          <th class="gender">Gender</th>
          <th class="university">Academy</th>
          <th class="field">Field</th>
          <th class="delete">Delete</th>
          <th class="update">Update</th>
        </tr>
        ${rows}
      `;
    })
    .catch(error => {
      error => console.error(error)
    });
}
render()