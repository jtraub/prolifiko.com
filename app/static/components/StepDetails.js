import React from 'react'
import Textarea from './Textarea'
import AbstractDetails from './AbstractDetails';

export class MidnightStepDetails extends AbstractDetails {
    static HEADING = 'Set Your Step';

    componentWillMount() {
        this.setDataPrefix('step');

        const value = {
            1: 'First',
            2: 'Second',
            3: 'Third',
            4: 'Fourth',
            5: 'Fifth'
        }[this.props.stepNumber] + ' Step';

        this.onNameChange({ target: { value } });
    }

    render() {
        const stepDescription = this.getDescription();

        const { stepNumber } = this.props;
        let intro, tip;
        let placeholder = 'Tip: Don’t think about the project as a whole. Just think ' +
            'about the one thing you can do next to progress your writing.';

        if (stepNumber === 1) {
            intro = (
                <section>
                    <p>What's the first step you can take to achieve your 5-day writing goal?</p>
                </section>
            );

            tip = (
                <section>
                    <p>
                        Still struggling? Check out our resources on&nbsp;
                        <a href="http://blog.write-track.co.uk/how-to-set-your-first-step/" target="_blank">how to set a first step</a>.
                    </p>
                </section>
            );
        } else if (stepNumber === 2) {
            intro = (
                <section>
                    <p>Way to go! That’s amazing!</p>

                    <p>What's the next step you can take to achieve your 5-day writing goal? Tell us below.</p>
                </section>
            );
        } else if (stepNumber === 3) {
            intro = (
                <section>
                    <p>Well done!</p>

                    <p>What's the third step you can make progress on your goal?</p>
                </section>
            );


            placeholder = 'Tip: Note down what small action you\'re going ' +
                'to take next. If you struggled with the last step, be nice ' +
                'to yourself, and set a smaller step.';
        } else if (stepNumber === 4) {
            intro = (
                <section>
                    <p>Amazing! You've completed three steps are you're well over half way. Only two steps remain.</p>

                    <p>What's the fourth step you can take to move your project forward?</p>
                </section>
            );


            placeholder = 'Tip: Think small but achievable. What one thing ' +
                'can you do next to progress your writing?';
        } else {
            intro = (
                <section>
                    <p>You've completed four steps – amazing! Just one final push to complete this challenge.</p>

                    <p>What's the final step you can take?</p>
                </section>
            );

            placeholder = 'Tip: You might be nearly there but don\'t think ' +
                'too big - keep it small. What one final step will move your ' +
                'project forward?';
        }

        return (
            <div className="form--inline">
               {intro}

                <div className="form__input">
                    <Textarea
                        onChange={this.onDescriptionChange.bind(this)}
                        placeholder={placeholder}
                        name="stepDescription"
                        value={stepDescription || ''}
                    />
                </div>

                {tip}
            </div>
        );
    }
}

export class CustomStepDetails extends AbstractDetails {
    static HEADING = 'Set Your Step';

    componentWillMount() {
        this.setDataPrefix('step');
    }

    componentDidMount() {
        this.onDescriptionChange(this.getDescription(), this.description.isValid());
    }

    render() {
        const stepName = this.getName();
        const stepDescription = this.getDescription();

        const { stepNumber } = this.props;
        let intro;
        let namePlaceholder = 'Tip: Don’t think about the project as a whole. Just think ' +
            'about what you can achieve in your next writing session.';
        let descriptionPlaceholder = 'Use this box to give your step a longer description ' +
            'or make any notes. You can refer to your notes in your dashboard.';

        if (stepNumber === 1) {
            intro = (
                <section>
                    <p>Briefly describe the first step you're going to take to meet your writing goal.</p>
                </section>
            );
        } else if (stepNumber === 2) {
            intro = (
                <section>
                    <p>Now, it's time to set another step:</p>
                </section>
            );

            namePlaceholder = 'What are you going to achieve in your next ' +
                'writing session? All those steps will build up. Just think ' +
                'one step at a time.'
        }

        const { nameCharsRemaining } = this.state;
        let charLimitColor = 'inherit';

        if (nameCharsRemaining < 0) {
            charLimitColor = 'red';
        }

        return (
            <div className="form--inline">
                {intro}

                <div className="form__input">
                    <textarea
                        rows={4}
                        placeholder={namePlaceholder}
                        onChange={this.onNameChange.bind(this)}
                        name="stepName"
                        value={stepName || ''}
                    />
                    <p style={{ color: charLimitColor }}>{nameCharsRemaining} characters remaining</p>
                </div>

                <section>
                    <p>Want more space to describe your step?</p>
                </section>

                <div className="form__input">
                    <Textarea
                        required={false}
                        onChange={this.onDescriptionChange.bind(this)}
                        placeholder={descriptionPlaceholder}
                        name="stepDescription"
                        value={stepDescription || ''}
                        ref={ref => this.description = ref}
                    />
               </div>

                <section>
                    <p>
                        Need some tips on setting a step? Check out this video. <a href="https://youtu.be/MMlU6NEnxpg" target="_blank">Watch the video</a>
                    </p>
                </section>
            </div>
        );
    }
}

