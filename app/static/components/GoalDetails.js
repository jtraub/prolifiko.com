import React from 'react';
import Textarea from './Textarea';

export default class GoalDetails extends React.Component {
    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
    };

    static defaultProps = {
        data: {}
    };

    state = {
        isValid: false,
    };

    next(event) {
        event.preventDefault();

        this.props.next({
            goalName: this._name.value,
            goalDescription: this._textarea.getValue(),
        }, this.state.isValid);
    }

    render() {
        const placeholder = 'Tip: What you write is up to you but try to be specific, eg ' +
            'you might want to write for an amount of time or to a word ' +
            'count, or on a specific project.';

        const { goalName, goalDescription } = this.props.data;

        return (
            <div className="page">
                <section>
                    <p>Welcome to the challenge! It’s great to have you on
                        board.</p>

                    <p>Your first task is to set a writing goal.</p>

                    <p><strong>What do you want to achieve with your writing in
                        the next 5 days?</strong></p>
                </section>

                Goal Name: <input ref={input => this._name = input} type="text" defaultValue={goalName} />
                <Textarea
                    ref={input => this._textarea = input}
                    onChange={isValid => this.setState({ isValid })}
                    placeholder={placeholder} />

                <section>
                    <p>Still struggling? Check out our blog on <a
                        href="http://blog.write-track.co.uk/how-to-set-a-writing-goal/">how
                        to set a goal</a>.</p>

                    <p>All done? Great! Next, you need to set a step to help
                        you achieve your goal.</p>
                </section>
            </div>
        );
    }
}