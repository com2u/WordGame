// Beispiel-JSON-Struktur
// Beispiel-JSON-Struktur
// Globale Variable, um die vom Server empfangenen Daten zu speichern
var data = {{ data }};

let mixArea;
let isDragging = false;
console.log(document.domain);
console.log(location.port);


var socket = io.connect('http://' + document.domain + ':' + location.port);
//var socket = io.connect('http://localhost:5000' );

/* Empfangen der initialen Daten vom Server und Initialisieren der UI
socket.on('initial_data', function(server_json_data) {
    data = server_json_data;  // Aktualisieren der lokalen Daten mit den Daten vom Server
    initializeUI();  // Funktion, die Ihre UI initialisiert, z.B. Objekte zeichnen, Event-Listener hinzufügen, etc.
});
*/

// Funktion, die aufgerufen wird, wenn aktualisierte Daten vom Server empfangen werden
//socket.on('refresh_data', function(updated_json_data) {
socket.on(`${data.token}`, function(updated_json_data) {
   // data = updated_json_data;  // Aktualisieren der lokalen Daten mit den neuen Daten vom Server
    console.log(updated_json_data);
    try {
        console.log('Convert JSON Data');
        data = JSON.parse(updated_json_data);
    } catch (error) {
        console.log('Convert JSON Data failed');
        data = updated_json_data;
    }


    console.log(data);
    updateUI()  // Funktion, die Ihre UI aktualisiert, z.B. Objekte neu zeichnet, basierend auf den neuen Daten
});

function updateUI() {
    // Entfernen aller Kinder eines bestimmten DOM-Elements
    // Wenn Sie einen Container für die Objekte haben, verwenden Sie dessen ID anstelle von 'body'
    let container = document.body; // Oder document.getElementById('IhrContainer');
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }

    // Aufrufen von initializeUI, um die Objekte basierend auf den aktualisierten Daten neu zu erstellen
    initializeUI();
}


// Funktion zum Senden von aktualisierten Daten an den Server
function sendDataToServer(updated_data) {
    socket.emit('update_data', updated_data);
}

// Setzen des Hintergrundbildes
document.body.style.backgroundImage = `url(${data.backgroundImage})`;
//document.body.style.backgroundSize = 'cover';
//document.body.style.height = '100vh';



function initializeUI() {
    console.log("initializeUI");
    console.log(data);

    try {
        // Setzen des Hintergrundbildes
        document.body.style.backgroundImage = `url(${data.backgroundImage})`;
        document.body.style.backgroundRepeat = 'no-repeat';
        document.body.style.backgroundSize = 'auto'; /* Verhindert die Skalierung des Bildes */
        document.body.style.backgroundPosition = 'top left'; /* Bild beginnt in der oberen linken Ecke */
        document.body.style.overflow = 'auto'; /* Ermöglicht das Scrollen, wenn das Bild größer als der Viewport ist */


    // Erstellen der HTML-Elemente für jedes Objekt
    // Hinzufügen eines Divs für den Mix-Bereich
        let mixArea = document.createElement("div");
        mixArea.style.position = 'absolute';
        mixArea.style.left = `${data.MixArea.X}px`;
        mixArea.style.top = `${data.MixArea.Y}px`;
        mixArea.style.width = `${data.MixArea.Width}px`;
        mixArea.style.height = `${data.MixArea.Height}px`;
        mixArea.style.border = '3px dashed #000000';
        mixArea.ondblclick = mixZIndices;
        document.body.appendChild(mixArea);

    // Erstellen der HTML-Elemente für jedes Objekt
    // Hinzufügen eines Divs für den Mix-Bereich
        let flipArea = document.createElement("div");
        flipArea.style.position = 'absolute';
        flipArea.style.left = `${data.FlipArea.X}px`;
        flipArea.style.top = `${data.FlipArea.Y}px`;
        flipArea.style.width = `${data.FlipArea.Width}px`;
        flipArea.style.height = `${data.FlipArea.Height}px`;
        flipArea.style.border = '3px dashed #AAAA00';
        flipArea.ondblclick = flipAll;
        document.body.appendChild(flipArea);


        // Hinzufügen eines Divs für den UpdateImageIndexArea-Bereich
        let updateImageIndexArea = document.createElement("div");
        updateImageIndexArea.style.position = 'absolute';
        updateImageIndexArea.style.left = `${data.UpadteImageIndexArea.X}px`;
        updateImageIndexArea.style.top = `${data.UpadteImageIndexArea.Y}px`;
        updateImageIndexArea.style.width = `${data.UpadteImageIndexArea.Width}px`;
        updateImageIndexArea.style.height = `${data.UpadteImageIndexArea.Height}px`;
        updateImageIndexArea.style.border = '3px dashed #FF0000';
        document.body.appendChild(updateImageIndexArea);

        selectArea();

        function mixZIndices() {
            console.log('Mix');
            let mixAreaBounds = mixArea.getBoundingClientRect();

            // Identifizieren der Objekte innerhalb des Mix-Bereichs
            let innerObjects = data.Objects.filter((obj, idx) => {
                let objDiv = document.querySelectorAll('.object')[idx];
                let objBounds = objDiv.getBoundingClientRect();

                return (
                    objBounds.top > mixAreaBounds.top &&
                    objBounds.bottom < mixAreaBounds.bottom &&
                    objBounds.left > mixAreaBounds.left &&
                    objBounds.right < mixAreaBounds.right
                );
            });

            console.log(innerObjects);

            // Mischen der Z-Werte der inneren Objekte
            let zIndices = innerObjects.map(obj => obj.Z);
            zIndices.sort(() => Math.random() - 0.5);

            innerObjects.forEach((obj, idx) => {
                obj.Z = zIndices[idx];
                document.querySelectorAll('.object')[data.Objects.indexOf(obj)].style.zIndex = obj.Z;
            });
            sendDataToServer(data);
        }

        function flipAll() {
            console.log('FlipAll');
            let flipAreaBounds = flipArea.getBoundingClientRect();

            // Identifizieren der Objekte innerhalb des Mix-Bereichs
            let innerObjects = data.Objects.filter((obj, idx) => {
                let objDiv = document.querySelectorAll('.object')[idx];
                let objBounds = objDiv.getBoundingClientRect();

                return (
                    objBounds.top > flipAreaBounds.top &&
                    objBounds.bottom < flipAreaBounds.bottom &&
                    objBounds.left > flipAreaBounds.left &&
                    objBounds.right < flipAreaBounds.right
                );
            });

            console.log(innerObjects);

            // Mischen der Z-Werte der inneren Objekte
            //let zIndices = innerObjects.map(obj => obj.Z);
            //zIndices.sort(() => Math.random() - 0.5);
            console.log('FlipAll');
            innerObjects.forEach((obj, idx) => {
                obj.currentImageIndex = (obj.currentImageIndex + 1) % obj.Image.length;
                let objDiv = document.querySelectorAll('.object')[idx];
                objDiv.querySelector('img').src = obj.Image[obj.currentImageIndex];

                //obj.Z = zIndices[idx];
                //document.querySelectorAll('.object')[data.Objects.indexOf(obj)].style.zIndex = obj.Z;
            });
            sendDataToServer(data);
        }


        // Sortieren der Objekte nach der Z-Position
        data.Objects.sort((a, b) => a.Z - b.Z);

         // Objekte erstellen
        data.Objects.forEach((object, index) => {
            let element = createObjectElement(object, index, mixArea, updateImageIndexArea, flipArea);
            document.body.appendChild(element);
        });
    }
    catch(err) {
        console.log('ERROR initializeUI');
        console.log(err);
        console.log(data);
    }
}


function createObjectElement(object, index, mixArea, updateImageIndexArea, flipArea) {
    let div = document.createElement('div');
    div.id = 'object-' + index;
    //div.className = 'draggable';
    div.classList.add("object");
    div.style.left = object.X + 'px';
    div.style.top = object.Y + 'px';
    div.style.zIndex = object.Z;
    div.style.position = 'absolute';
    div.style.color = object.Color;
    div.style.fontSize = object.Size + 'px';
    console.log('init Object');
    console.log(object.currentImageIndex);
    console.log(object.Text);
    //let img = new Image();





    switch(object.Type) {
        case 'text':
            div.innerHTML = `
                <img src="${object.Image[object.currentImageIndex]}" alt="Objekt-Bild">
                <img src="${object.Image[object.currentImageIndex]}" alt="Objekt-Bild">
                <div style="display: flex; justify-content: center; align-items: center; color: ${object.Color ? object.Color : ''}; font-size: ${object.Size}px; position: absolute; text-align: center;">
                    ${object.Text ? object.Text : ''}
                </div>
                <div class="rotate-icon-right"></div>
                <div class="rotate-icon-left"></div>
            `;
            div.querySelector('img').style.transform = `rotate(${object.Rotate}deg)`;
            div.querySelector('img').onload = function() {
                // Once the image is loaded, set the dimensions of the div
                div.style.width = this.width + 'px';
                div.style.height = this.height + 'px';
                console.log("Object resize on load");
                // Depending on your layout requirements, you might need to adjust other properties
            };

            addContextMenu(div);
            //console.log(object.Rotate);
            break;
        case 'input':
            // Set the innerHTML of the div using a template literal
            div.innerHTML = `
                <!-- The rest of your HTML structure can follow, if needed -->

                <img src="${object.Image ? object.Image[object.currentImageIndex] : ''}" alt="Object Image" >
                <input type="text" value="${object.Value}" style="font-size: ${object.Size}px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);" id="myTextInput">
                <p style="color: ${object.Color ? object.Color : ''}; font-size: ${object.Size}px; position: absolute; top: 0%">${object.Text ? object.Text : ''}</p>
                <div class="rotate-icon-right"></div>
                <div class="rotate-icon-left"></div>
            `;
            div.querySelector('img').style.transform = `rotate(${object.Rotate}deg)`;
            div.querySelector('img').onload = function() {
                // Once the image is loaded, set the dimensions of the div
                div.style.width = this.width + 'px';
                div.style.height = this.height + 'px';
                console.log("Input Object resize on load");
                console.log(this.width);
                // Depending on your layout requirements, you might need to adjust other properties
            };
            // Now, select the input element and attach an onchange event listener to it
            let input = div.querySelector('#myTextInput');

            input.onchange = function() {
                object.Value = this.value;
                console.log("Input Updated");
                sendDataToServer(data); // assuming sendDataToServer is a function that you've defined elsewhere
            };
            div.appendChild(input);
            break;
        case 'checkbox':
            // Set the innerHTML of the div using a template literal
        div.innerHTML = `
            <img src="${object.Image ? object.Image[object.currentImageIndex] : ''}" alt="Object Image" >
            <input type="checkbox" ${object.Value ? 'checked' : ''} id="myCheckbox" style="font-size: ${object.Size}px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);" id="myTextInput">
            <p style="color: ${object.Color ? object.Color : ''}; font-size: ${object.Size}px; position: absolute; top: 0%">${object.Text ? object.Text : ''}</p>
            <div class="rotate-icon-right"></div>
            <div class="rotate-icon-left"></div>
        `;

        div.querySelector('img').style.transform = `rotate(${object.Rotate}deg)`;
        div.querySelector('img').onload = function() {
                // Once the image is loaded, set the dimensions of the div
                div.style.width = this.width + 'px';
                div.style.height = this.height + 'px';
                console.log("Input Object resize on load");
                console.log(this.width);
                // Depending on your layout requirements, you might need to adjust other properties
            };

        // Append the div to the body or another parent element if needed
        //document.body.appendChild(div);

        // Now, select the checkbox input element and attach an onchange event listener to it
        let checkbox = div.querySelector('#myCheckbox');

        checkbox.onchange = function() {
            object.Value = this.checked ? 'true' : 'false'; // 'checked' property is true if the checkbox is checked, and false otherwise
            console.log("Checkbox Updated");
            sendDataToServer(data); // assuming sendDataToServer is a function that you've defined elsewhere
        };
            div.appendChild(checkbox);
            break;
    }


    //let isDragging = false;  // Zustand, ob das Objekt gerade gezogen wird


	// Drag & Drop
    div.onmousedown = function(e) {
    	console.log('Drag');
        let offsetX = e.clientX - div.getBoundingClientRect().left;
        let offsetY = e.clientY - div.getBoundingClientRect().top;

        function onMouseMove(e) {
    		console.log('Move');
            div.style.left = e.clientX - offsetX + "px";
            div.style.top = e.clientY - offsetY + "px";
            isDragging = false;
        }

        function onMouseUp() {
			console.log('EndDrag');
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);

            // Aktualisieren der JSON-Struktur
            data.Objects[index].X = div.offsetLeft;
            data.Objects[index].Y = div.offsetTop;
            //data.Objects[index].Rotate = div.Rotate;
            //data.Objects[index].currentImageIndex = div.currentImageIndex;

            sendDataToServer(data);
        }

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    };





    // Rotation um 90 Grad im Uhrzeigersinn
    div.querySelector('.rotate-icon-right').onclick = function(e) {
        console.log(object.Rotate);
		object.Rotate = (object.Rotate + 90) % 360;
        //data.Objects[index].Rotate = (object.Rotate + 90) % 360;
        div.querySelector('img').style.transform = `rotate(${object.Rotate}deg)`;
		console.log('Rotate right');
		sendDataToServer(data);
    };

    // Rotation um 90 Grad gegen den Uhrzeigersinn
    div.querySelector('.rotate-icon-left').onclick = function(e) {
        object.Rotate = (object.Rotate - 90) % 360;
        //data.Objects[index].Rotate = (object.Rotate + 90) % 360;
        div.querySelector('img').style.transform = `rotate(${object.Rotate}deg)`;
		console.log('Rotate left');
		sendDataToServer(data);

    };

	div.ondblclick = function() {
        // Bildwechsel-Logik


        // Prüfen, ob das Objekt sich innerhalb des Mix-Bereichs befindet
        let objectBounds = div.getBoundingClientRect();
        let mixAreaBounds = mixArea.getBoundingClientRect();
		let updateImageIndexAreaBounds = updateImageIndexArea.getBoundingClientRect();

		if (
            objectBounds.top > updateImageIndexAreaBounds.top &&
            objectBounds.bottom < updateImageIndexAreaBounds.bottom &&
            objectBounds.left > updateImageIndexAreaBounds.left &&
            objectBounds.right < updateImageIndexAreaBounds.right
        ) {
            // Setzen eines zufälligen currentImageIndex und Aktualisieren des Bildes
			console.log('Random');

            object.currentImageIndex = Math.floor(Math.random() * object.Image.length);
            div.querySelector('img').src = object.Image[object.currentImageIndex];
            data.Objects[index].currentImageIndex = object.currentImageIndex;
        } else {
            // Standard Bildwechsel-Logik hier...
			console.log('Flip');
            object.currentImageIndex = (object.currentImageIndex + 1) % object.Image.length;
            div.querySelector('img').src = object.Image[object.currentImageIndex];
            //data.Objects[index].currentImageIndex = object.currentImageIndex;
        }


        if (
            objectBounds.top > mixAreaBounds.top &&
            objectBounds.bottom < mixAreaBounds.bottom &&
            objectBounds.left > mixAreaBounds.left &&
            objectBounds.right < mixAreaBounds.right
        ) {
            // Wenn ja, Z-Reihenfolge der Objekte im Mix-Bereich mischen

            //mixZIndices();
        } else {


		}
		sendDataToServer(data);
    };





    return div;
}

function selectArea(){
// Global variables to keep track of the drag status and positions

    let dragStartX = 0;
    let dragStartY = 0;
    let dragEndX = 0;
    let dragEndY = 0;

    // Create a div to represent the selected area
    let selectionArea = document.createElement('div');
    selectionArea.style.position = 'absolute';
    selectionArea.style.border = '1px solid #000';
    selectionArea.style.backgroundColor = 'rgba(0, 0, 255, 0.2)';
    selectionArea.style.display = 'none';
    document.body.appendChild(selectionArea);

    // Function to handle the mousedown event
    function onMouseDown(event) {
        isDragging = true;
        dragStartX = event.clientX;
        dragStartY = event.clientY;
    }

    // Function to handle the mousemove event
    function onMouseMove(event) {
        if (!isDragging) return;

        // Update the end position
        dragEndX = event.clientX;
        dragEndY = event.clientY;

        // Update the position and size of the selectionArea div
        const minX = Math.min(dragStartX, dragEndX);
        const minY = Math.min(dragStartY, dragEndY);
        const width = Math.abs(dragStartX - dragEndX);
        const height = Math.abs(dragStartY - dragEndY);

        selectionArea.style.left = minX + 'px';
        selectionArea.style.top = minY + 'px';
        selectionArea.style.width = width + 'px';
        selectionArea.style.height = height + 'px';
        selectionArea.style.display = 'block';
    }

    // Function to handle the mouseup event
    function onMouseUp(event) {
        if (!isDragging) return;

        isDragging = false;
        selectionArea.style.display = 'none'; // Hide the selection area

        // Compute the selection area boundaries
        const minX = Math.min(dragStartX, dragEndX);
        const minY = Math.min(dragStartY, dragEndY);
        const maxX = Math.max(dragStartX, dragEndX);
        const maxY = Math.max(dragStartY, dragEndY);

        // Find elements within the selection area
        let elementsWithinSelection = [];
        const elements = document.querySelectorAll('*'); // Get all elements
        elements.forEach(element => {
            const rect = element.getBoundingClientRect();

            // Check if the element is within the selection bounds
            if (rect.left >= minX && rect.right <= maxX && rect.top >= minY && rect.bottom <= maxY) {
                elementsWithinSelection.push(element);
            }
        });

        // Do something with elementsWithinSelection, e.g., print to console or display to the user
        console.log(elementsWithinSelection);
    }

    // Attach the event listeners
    document.addEventListener('mousedown', onMouseDown);
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
}

function addContextMenu(div){
            let contextMenu = document.createElement('div');
            contextMenu.innerHTML = `
                <ul style="list-style-type:none; padding: 10px; background-color: #f0f0f0; border: solid 1px #ccc;">
                    <li id="deleteObject" style="cursor:pointer; margin-bottom: 5px;">Delete</li>
                    <li id="cloneObject" style="cursor:pointer; margin-bottom: 5px;">Clone</li>
                    <li id="nextImage" style="cursor:pointer; margin-bottom: 5px;">Next Image</li>
                    <li id="randomImage" style="cursor:pointer;">Random Image</li>
                </ul>
            `;
            contextMenu.style.position = 'absolute'; // Use absolute positioning
            contextMenu.style.display = 'none'; // Initially don't display it
            contextMenu.style.zIndex = '1000'; // Ensure it's on top of other elements
            document.body.appendChild(contextMenu); // Append it to the body


                        // Function to handle the right-click event on your object
            function onObjectRightClicked(event) {
                event.preventDefault(); // Prevent the default context menu from appearing
                // Get the bounding rectangle of the target object
                const rect = event.target.getBoundingClientRect();
                // Position your custom context menu at the top left of the object
                contextMenu.style.left = rect.left + 'px';
                contextMenu.style.top = rect.top + 'px';
                contextMenu.style.display = 'block'; // Display the menu
            }

            // Attach the right-click event handler to your object
            //let yourObject = document.getElementById('yourObjectId'); // Replace with your actual object's ID
            div.addEventListener('contextmenu', onObjectRightClicked);

            // Function to handle clicking on the context menu options
            function onContextMenuOptionClicked(event) {
                contextMenu.style.display = 'none'; // Hide the context menu

                switch(event.target.id) {
                    case 'deleteObject':
                        // Code to delete the object
                        break;
                    case 'cloneObject':
                        // Code to clone the object
                        break;
                    case 'nextImage':
                        // Code to show the next image
                        break;
                    case 'randomImage':
                        // Code to show a random image
                        break;
                }
            }

            // Attach the click event handler to the context menu
            contextMenu.addEventListener('click', onContextMenuOptionClicked);

            // Optional: Hide the context menu when clicking elsewhere
            window.addEventListener('click', function(event) {
                if (event.target !== contextMenu) {
                    contextMenu.style.display = 'none';
                }
            });

}
