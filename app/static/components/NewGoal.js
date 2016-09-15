import React from 'react'
import Textarea from './Textarea';

class SetGoal extends React.Component {
    static propTypes = {
        next: React.PropTypes.func.isRequired,
    };

    state = {
        isValid: false,
    };

    next(event) {
        this.props.next({ text: this._textarea.getValue() });
        event.preventDefault();
    }

    render() {
        const placeholder = 'Tip: What you write is up to you but try to be specific, eg ' +
                            'you might want to write for an amount of time or to a word ' +
                            'count, or on a specific project.';

        return (
            <div className="page">
                <section>
                    <p>Welcome to the challenge! It’s great to have you on
                        board.</p>

                    <p>Your first task is to set a writing goal.</p>

                    <p><strong>What do you want to achieve with your writing in
                        the next 5 days?</strong></p>
                </section>

                <div>
                    <Textarea
                        ref={input => this._textarea = input}
                        onChange={isValid => this.setState({ isValid })}
                        placeholder={placeholder}
                    ></Textarea>
                </div>

                <section>
                    <p>Still struggling? Check out our blog on <a
                        href="http://blog.write-track.co.uk/how-to-set-a-writing-goal/">how
                        to set a goal</a>.</p>

                    <p>All done? Great! Next, you need to set a step to help
                        you achieve your goal.</p>
                </section>

                <p>
                    <button className="gutter" disabled={!this.state.isValid} onClick={this.next.bind(this)}>Next &raquo;</button>
                </p>
            </div>
        );
    }
}

class FirstStep extends React.Component {
    static propTypes = {
        next: React.PropTypes.func.isRequired,
        prev: React.PropTypes.func.isRequired,
    };

    state = {
        isValid: false,
    };

    next(event) {
        this.props.next({ firstStep: this._textarea.getValue() });
        event.preventDefault();
    }

    prev(event) {
        this.props.prev({ firstStep: this._textarea.getValue() });
        event.preventDefault();
    }

    render() {
        const placeholder = 'Tip: Don’t think about the project as a whole. Just think ' +
                            'about the one thing you can do next to progress your writing.';
        return (
            <div>
                <p>What’s the first step you can take to achieve your 5-day writing goal?</p>

                <div>
                    <Textarea
                        ref={input => this._textarea = input}
                        onChange={isValid => this.setState({ isValid })}
                        placeholder={placeholder}
                    ></Textarea>
                </div>

                <section>
                    <p>Still struggling? Check out our blog on <a href="http://blog.write-track.co.uk/how-to-set-your-first-step/">how to set a first step</a>.</p>

                    <p>
                        <button className="gutter" onClick={this.prev.bind(this)}>&laquo; Previous</button>
                        <button className="gutter" disabled={!this.state.isValid} onClick={this.next.bind(this)}>Next &raquo;</button>
                    </p>
                </section>
            </div>
        );
    }
}

class Timezone extends React.Component {
    static propTypes = {
        prev: React.PropTypes.func.isRequired,
        submit: React.PropTypes.func.isRequired,
    };

    state = {
        timezone: null,
    };

    componentWillMount() {
        const guess = moment.tz.guess();
        this.setState({ timezone: guess });
    }

    onChange(event) {
        this.setState({ timezone: event.target.value });
    }

    prev(event) {
        this.props.prev({ timezone: this.state.timezone });
        event.preventDefault();
    }

    submit(event) {
        this.props.submit({ timezone: this.state.timezone });
        event.preventDefault();
    }

    render() {
        return (
            <div>
                <p>One last thing - to make sure we set you the right deadline we need to know your timezone.
                    We've made our best guess, but if it's not right please select the correct one from this list:</p>

                <select value={this.state.timezone} onChange={this.onChange.bind(this)}>
                    {this.props.options.map(option => <option key={option} value={option}>{option}</option>)}
                </select>

                <p>All done? Let's get going.</p>

                <p>
                    <button className="gutter" onClick={this.prev.bind(this)}>&laquo; Previous</button>
                    <button className="gutter" onClick={this.submit.bind(this)}>Start! &raquo;</button>
                </p>
            </div>
        );
    }
}

export default class NewGoal extends React.Component {
    static propTypes = {
        csrfToken: React.PropTypes.string.isRequired,
        timezones: React.PropTypes.array.isRequired,
    };

    state = {
        page: 1,
        text: '',
        firstStep: '',
        timezone: '',
    };

    constructor() {
        super();

        this.next = this.next.bind(this);
        this.prev = this.prev.bind(this);
        this.submit = this.submit.bind(this);
    }

    next(newState) {
        newState.page = this.state.page + 1;
        this.setState(newState);
    }

    prev(newState) {
        newState.page = this.state.page - 1;
        this.setState(newState);
    }

    submit(newState) {
        this.setState(newState, () => {
            this._form.submit()
        });
    }

    shouldComponentUpdate(nextState) {
        return this.state.page !== nextState.page;
    }

    render() {
        const { page } = this.state;

        let content;
        switch (page) {
            case 1:
                content = <SetGoal next={this.next}/>;
                break;
            case 2:
                content = <FirstStep next={this.next} prev={this.prev}/>;
                break;
            case 3:
                content = <Timezone submit={this.submit} prev={this.prev} options={this.props.timezones}/>;
                break;
        }

        return (
            <div>
                {content}
                <form method="post" style={{display: 'none'}} ref={form => this._form = form}>
                    <input type="hidden" name="csrfmiddlewaretoken" value={this.props.csrfToken}/>
                    <input type="hidden" name="text" value={this.state.text}/>
                    <input type="hidden" name="first_step" value={this.state.firstStep}/>
                    <input type="hidden" name="timezone" value={this.state.timezone}/>
                </form>
            </div>
        );
    }
}

