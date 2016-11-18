import React from 'react';
import Textarea from './Textarea';
import AbstractDetails from './AbstractDetails';

export class FiveDayChallengeDetails extends AbstractDetails {

    componentWillMount() {
        this.setDataPrefix('goal');

        const value = 'Five Day Challenge';

        this.onNameChange({ target: { value } });
    }

    render() {
        const goalDescription = this.getDescription();

        const placeholder = 'Tip: What you write is up to you but try to be ' +
            'specific, eg you might want to write for an amount of time or to a ' +
            'word count, or on a specific project.';

        return (
            <div className="page form--inline">
                <section>
                    <p>Welcome to the challenge! It’s great to have you on
                        board.</p>

                    <p>Your first task is to set a writing goal.</p>

                    <p><strong>What do you want to achieve with your writing in
                        the next 5 days?</strong></p>
                </section>

                <div className="form__input">
                    <Textarea
                        onChange={this.onDescriptionChange.bind(this)}
                        placeholder={placeholder}
                        name="goalDescription"
                        value={goalDescription || ''}
                        />
                </div>

                <section>
                    <p>
                        Still struggling? Check out our resources on
                        <a href="http://blog.write-track.co.uk/how-to-set-a-writing-goal/" target="_blank">
                            how to set a goal.
                        </a>
                    </p>

                    <p>All done? Great! Next, you need to set a step to help
                        you achieve your goal.</p>
                </section>
            </div>
        );
    }
}

export class CustomGoalDetails extends AbstractDetails {
    static HEADING = 'Set Your Goal';

    componentWillMount() {
        this.setDataPrefix('goal');
    }

    render() {
        const goalName = this.getName();
        const goalDescription = this.getDescription();

        const descPlaceholder = 'Tip: Don’t be too adventurous at this stage. Make' +
            ' your writing goal something you can achieve in four weeks or less.';

        const namePlaceholder= 'Tip: in 140 characters or less describe your goal. For example,' +
            ' this could be ‘outline and write chapter 1';

        const { nameCharsRemaining } = this.state;
        let charLimitColor = 'inherit';

        if (nameCharsRemaining < 0) {
            charLimitColor = 'red';
        }

        return (
            <div className="page form--inline">
                <section>
                    <p>What's your writing project? Describe your goal here.</p>
                </section>

                <div className="form__input">
                    <Textarea
                        onChange={this.onDescriptionChange.bind(this)}
                        placeholder={descPlaceholder}
                        name="goalDescription"
                        value={goalDescription || ''}
                    />
                </div>

                <section>
                    <p>Now, give this goal a short name.</p>
                </section>

                <div className="form__input">
                    <textarea
                        cols={40}
                        rows={5}
                        placeholder={namePlaceholder}
                        onChange={this.onNameChange.bind(this)}
                        name="goalName"
                        value={goalName || ''}
                    />
                    <p style={{ color: charLimitColor }}>{nameCharsRemaining} characters remaining</p>
                </div>

                <section>
                    <p>
                        Want a quick primer on goal setting? We’ve made this video just for you. <a href="https://youtu.be/2Ngdj5_j_5E" target="_blank">Watch the video</a>
                    </p>
                </section>
            </div>
        );
    }
}
