/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

/**
 * Card Component
 * A reusable component that displays content within a styled card layout
 * @extends Component
 */
export class Card extends Component {
    /**
     * Template identifier for the card component
     * References the XML template: awesome_owl.card
     */
    static template = "awesome_owl.card";

    /**
     * Props definition and validation
     * @property {string} title - The card's header title
     * @property {string} content - The main content to be displayed in the card body
     */
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: true
            },
        }
    };

    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }
}
