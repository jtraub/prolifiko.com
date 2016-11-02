import React from 'react';

export default class AbstractDetails extends React.Component {
    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
        data: React.PropTypes.object.isRequired,
        stepNumber: React.PropTypes.number,
    };

    static defaultProps = {
        data: {
            name: '',
            description: '',
        },
    };

    state = {
        isDescriptionValid: false,
        nameCharsRemaining: 140,
    };

    dataPrefix = null;

    setDataPrefix(prefix) {
        this.dataPrefix = prefix;
    }

    isValid(isDescriptionValid, name) {
        return isDescriptionValid && name && name.length && name.length <= 140;
    }

    onDescriptionChange(description, isDescriptionValid) {
        const isValid = this.isValid(isDescriptionValid, this.state.name);
        this.setState({ description, isDescriptionValid }, () => {
            const newData = {};
            newData[this.dataPrefix + 'Description'] = description;
            this.props.onChange(newData, isValid);
        });
    }

    onNameChange(event) {
        const name = event.target.value;
        const isValid = this.isValid(this.state.isDescriptionValid, name);
        const nameCharsRemaining = 140 - (name ? name.length : 0);
        const newState = { name, nameCharsRemaining, isValid };

        this.setState(newState, () => {
            const newData = {};
            newData[this.dataPrefix + 'Name'] = name;
            this.props.onChange(newData, newState.isValid);
        });
    }

    getName() {
        return this.state.name || this.props.data[this.dataPrefix + 'Name'];
    }

    getDescription() {
        return this.state.description || this.props.data[this.dataPrefix + 'Description'];
    }
}
