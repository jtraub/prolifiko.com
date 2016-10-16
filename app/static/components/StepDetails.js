import React from 'react'
import Textarea from './Textarea';

export default class StepDetails extends React.Component {
    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
        data: React.PropTypes.object.isRequired,
        stepNumber: React.PropTypes.number,
    };

    static defaultProps = {
        data: {
            stepName: '',
            stepDescription: '',
        }
    };

    state = {
        isValid: false,
    };

    onTextFieldChange(stepDescription, isValid) {
        this.setState({stepDescription, isValid}, () => {
            this.props.onChange({
                stepDescription,
            }, isValid);
        });
    }

    onNameChange(event) {
        const stepName = event.target.value
        this.setState({stepName}, () => {
            this.props.onChange({
                stepName,
            }, this.state.isValid);
        });
    }

    render() {
        const placeholder = 'Tip: Don’t think about the project as a whole. Just think ' +
            'about the one thing you can do next to progress your writing.';


        const stepName = this.state.stepName || this.props.data.stepName;
        const stepDescription = this.state.stepDescription || this.props.data.stepDescription;

        return (
            <div className="form--inline">
                <p>What’s the first step you can take to achieve your 5-day writing goal?</p>

                <div className="form__input">
                    <label>Name:</label>
                    <input
                        placeholder="Give your step a name."
                        onChange={this.onNameChange.bind(this)}
                        type="text"
                        name="stepName"
                        value={stepName || ''}
                    />
                </div>

                <div className="form__input">
                    <label>Description:</label>
                    <Textarea
                        onChange={this.onTextFieldChange.bind(this)}
                        placeholder={placeholder}
                        name="stepDescription"
                        value={stepDescription || ''}
                    />
                </div>

                <section>
                    <p>Still struggling? Check out our blog on <a
                        href="http://blog.write-track.co.uk/how-to-set-your-first-step/">how to set a first step</a>.
                    </p>
                </section>
            </div>
        );
    }
}
