/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

/**
 * Counter Component
 * A reusable component that displays a numeric value and allows incrementing it
 */
export class Counter extends Component {
    // Template used to render this component
    static template = "awesome_owl.counter";

    /**
     * Props definition for the Counter component
     * @property {Function} onChange - Optional callback function triggered when counter value changes
     */
    static props = {
        onChange: { type: Function, optional: true }
    };

    /**
     * Initialize component's reactive state
     * Sets up the initial counter value to 1
     */
    setup() {
        this.state = useState({ value: 1 });
    }

    /**
     * Increment counter value and notify parent component
     * Increases the counter by 1 and calls the onChange callback if provided
     */
    increment() {
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange();
        }
    }
}
