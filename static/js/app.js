const apiUrl = 'http://127.0.0.1:5000/apilist'; // URL API

// Функция для получения всех объектов
function fetchItems() {
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const itemList = document.getElementById('item-list');
            itemList.innerHTML = ''; // Очищаем список перед добавлением новых данных
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `ID: ${item.id} - Name: ${item.name} - Description: ${item.description}`;

                // Добавляем кнопку для обновления
                const updateButton = document.createElement('button');
                updateButton.textContent = "Update";
                updateButton.onclick = function () {
                    // При нажатии на "Update", заполняем поля для обновления
                    document.getElementById('update-id').value = item.id;
                    document.getElementById('update-name').value = item.name;
                    document.getElementById('update-description').value = item.description;
                };
                li.appendChild(updateButton);

                // Добавляем кнопку для удаления
                const deleteButton = document.createElement('button');
                deleteButton.textContent = "Delete";
                deleteButton.onclick = function () {
                    // При нажатии на "Delete", удаляем объект
                    deleteItem(item.id);
                };
                li.appendChild(deleteButton);

                itemList.appendChild(li);
            });
        })
        .catch(error => displayError(error));
}

// Функция для создания нового объекта
document.getElementById('create-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const description = document.getElementById('description').value;

    const body = JSON.stringify({name, description});

    fetch(apiUrl, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: body
    })
        .then(response => response.json())
        .then(data => displayResponse(data))
        .catch(error => displayError(error));
});

// Функция для обновления объекта
document.getElementById('update-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const id = document.getElementById('update-id').value;
    const name = document.getElementById('update-name').value;
    const description = document.getElementById('update-description').value;

    const body = JSON.stringify({name, description});

    fetch(`${apiUrl}/${id}`, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: body
    })
        .then(response => response.json())
        .then(data => displayResponse(data))
        .catch(error => displayError(error));
});

// Функция для удаления объекта
function deleteItem(id) {
    fetch(`${apiUrl}/${id}`, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => displayResponse(data))
        .catch(error => displayError(error));
}

// Функция для отображения ответа от API
function displayResponse(data) {
    const output = document.getElementById('response-output');
    output.textContent = JSON.stringify(data, null, 2);
}

// Функция для обработки ошибок
function displayError(error) {
    const output = document.getElementById('response-output');
    output.textContent = `Error: ${error}`;
}
