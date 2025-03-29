/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

/**
 * Main Playground Component
 * @class
 * @extends Component
 * @description Renders the main playground interface with Counter and Card components
 */
export class Playground extends Component {
    // Define the template to be used for rendering this component
    static template = "awesome_owl.playground";

    // Register child components that will be used in the template
    static components = { Counter, Card, TodoList };

    /**
     * Component initialization
     * @method
     * @description Sets up the initial state and content strings
     */
    setup() {
        // Regular HTML string (will be escaped)
        this.str1 = "<div class='text-primary'>some content</div>";

        // Marked as safe HTML (will not be escaped)
        this.str2 = markup("<div class='text-primary'>some content</div>");

        // Initialize reactive state for sum with initial value of 2
        this.sum = useState({ value: 2 });
    }

    /**
     * Increment the sum value
     * @method
     * @description Called by Counter components to update the total sum
     */
    incrementSum() {
        this.sum.value++;
    }
}
