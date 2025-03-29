/** @odoo-module **/

import { Component } from "@odoo/owl";

/**
 * TodoItem Component
 * Represents a single todo item in the list
 */
export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";

    /**
     * Props validation
     * @property {Object} todo - Todo item data (id, description, isCompleted)
     * @property {Function} toggleState - Function to toggle completion status
     * @property {Function} removeTodo - Function to delete todo
     */
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: {type: String, optional: true},
                isCompleted: Boolean
            }
        },
        toggleState: Function,
        removeTodo: Function,
    }

    /**
     * Handles checkbox change event
     */
    onChange() {
        this.props.toggleState(this.props.todo.id);
    }

    /**
     * Handles remove button click event
     */
    onRemove() {
        this.props.removeTodo(this.props.todo.id);
    }
}
