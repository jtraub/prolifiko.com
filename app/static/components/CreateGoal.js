import React from 'react'
import Textarea from './Textarea';
import DatePicker  from 'react-datepicker';
import moment from 'moment';
import _map from 'lodash.map';
import _each from 'lodash.each';
import GoalDetails from './GoalDetails';

export class GoalTarget extends React.Component {
    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
    };

    onChange(date) {
        this.props.onChange({ goalTarget: date.format('YYYY-MM-DD') }, true);
    }

    render() {
        let selected;

        if (this.props.data) {
            selected = moment(this.props.data.goalTarget);
        }

        return (
            <div>
                <section>
                    <p>Your first task to decide when you'd like to achieve this goal by.</p>

                    <p>We suggest you target 5-10 days.</p>
                </section>

                <DatePicker inline selected={selected} onChange={this.onChange.bind(this)} />
            </div>
        );
    }
}

export class StepDeadline extends React.Component {
    static propTypes = {
        prev: React.PropTypes.func.isRequired,
        submit: React.PropTypes.func.isRequired,
    };

    state = {
        deadline: null,
    };

    onChange(date) {
        this.setState({ target: date });
    }

    prev(event) {
        event.preventDefault();
        this.props.submit({ firstStepDeadline: this.state.target.format('YYYY-MM-DD') });
    }

    submit(event) {
        event.preventDefault();
        this.props.submit({ firstStepDeadline: this.state.target.format('YYYY-MM-DD') });
    }

    render() {
        const selected = moment().add(1, 'days');

        return (
            <div>
                <section>
                    <p>Choose a deadline for this step</p>

                    <p>We suggest you target 24-48 hours.</p>
                </section>

                <DatePicker inline selected={selected} onChange={this.onChange.bind(this)} />

                <section>
                    <p>
                        <button className="gutter" onClick={this.prev.bind(this)}>&laquo; Previous</button>
                        <button className="gutter" onClick={this.submit.bind(this)}>Submit &raquo;</button>
                    </p>
                </section>
            </div>
        );
    }
}

class Scene extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            pageIndex: 0,
            pages: props.pages.map(page => ({
                name: page.name,
                component: page,
            })),
            data: {},
        };
    }

    onChange(pageName, data, isValid) {
        const newData = Object.assign({}, this.state.data);

        newData[pageName] = { data, isValid };

        this.setState({ data: newData });
    }

    next() {
        this.setState({ pageIndex: this.state.page + 1 });
    }

    prev() {
        this.setState({ pageIndex: this.state.page - 1 });
    }

    submit() {
        this._form.submit();
    }

    render() {
        const pageIndex = this.state.page;
        const page = this.state.pages[pageIndex];
        const pageData = this.state.data[page.name];

        let inputs = [];

        _each(this.state.data, (pageData) => {
            _each(pageData.data, (value, name) => {
                inputs.push(<input type="hidden" name={name} value={value}/>);
            });
        });

        return (
            <div>
                {React.createElement(content, { onChange: this.onChange.bind(this, page.name), data: pageData.data, isValid: pageData.isValid })}
                {pageIndex === 0 && <button disabled={!this.state.isValid} onClick={this.next}>Next</button>}
                {pageIndex > 0 && pageIndex < pages.length - 1 && <button onClick={this.prev}>Previous</button>}
                {pageIndex === pages.length - 1 && <button disabled={!this.state.isValid} onClick={this.submit}>Submit</button>}

                <form method="post" style={{display: 'none'}} ref={form => this._form = form}>
                    {inputs}
                </form>
            </div>
        )
    }
}

export default function CreateGoal() {
    return <Scene pages={[GoalTarget, GoalDetails]} />;
}