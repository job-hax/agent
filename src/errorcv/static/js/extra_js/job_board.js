// get all board columns
const columns = document.getElementsByClassName("board-column")

// add all board columns into the containers array for dragula to use
var containers = []

for (var i=0; i < columns.length; i++) {
   containers.push(columns[i])
}

// initialize dragula
var board = dragula(containers)

// dragula event handlers
board.on("drop", (element, target, source) => {
   // get the item's unique identifier
   var item = element.dataset["id"]
   
   // get the item's old column name
   var oldColumn = source.dataset["name"]
   
   // get the item's new column name
   var newColumn = target.dataset["name"]
  
   console.log(`Item, ${item}, has been removed from the ${oldColumn} column.`)
   console.log(`Item, ${item}, has been added to the ${newColumn} column.`)
})