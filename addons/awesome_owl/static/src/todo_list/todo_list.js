/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutofocus } from "../utils";

/**
 * TodoList Component
 * A component that manages a list of todo items with add, toggle, and delete functionality
 * @extends Component
 */
export class TodoList extends Component {
    // Define the template to be used for rendering this component
    static template = "awesome_owl.todolist";

    // Register TodoItem as a child component
    static components = { TodoItem };

    /**
     * Initialize component's state and setup autofocus
     * @method
     * Sets up:
     * - Autofocus on the add-todo input field
     * - Reactive state for todos array
     */
    setup() {
        useAutofocus('add-todo');
        this.todos = useState([]);
    }

    /**
     * Add a new todo item when Enter key is pressed
     * @method
     * @param {KeyboardEvent} eve - The keyboard event object
     * Creates a new todo with:
     * - Unique ID based on current list length
     * - Description from input value
     * - Initial completion status as false
     */
    addTodo(eve) {
        if (eve.keyCode === 13 && eve.target.value != "") {
            this.todos.push({
                id: (this.todos?.length ?? 0) + 1,
                description: eve.target.value,
                isCompleted: false
            });
            eve.target.value = "";
        }
    }

    /**
     * Toggle the completion status of a todo item
     * @method
     * @param {number} todoId - The ID of the todo to toggle
     */
    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    /**
     * Remove a todo item from the list
     * @method
     * @param {number} todoId - The ID of the todo to remove
     */
    trashTodo(todoId) {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
