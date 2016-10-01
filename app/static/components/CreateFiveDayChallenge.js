import React from 'react'
import CreateStep from './CreateStep';
import GoalDetails from './GoalDetails';

export default class CreateFiveDayChallenge extends React.Component {
    static propTypes = {
        csrfToken: React.PropTypes.string.isRequired,
    };

    state = {
        page: 1,
        text: '',
        firstStep: '',
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
                content = <GoalDetails next={this.next}/>;
                break;
            case 2:
                content = <CreateStep prev={this.prev} submit={this.submit}/>;
                break;
        }

        return (
            <div>
                {content}
                <form method="post" style={{display: 'none'}} ref={form => this._form = form}>
                    <input type="hidden" name="csrfmiddlewaretoken" value={this.props.csrfToken}/>
                    <input type="hidden" name="text" value={this.state.text}/>
                    <input type="hidden" name="first_step" value={this.state.firstStep}/>
                </form>
            </div>
        );
    }
}

