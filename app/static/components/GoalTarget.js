import React from 'react';
import moment from 'moment';
import DatePicker  from 'react-datepicker';
import { setHeading } from '../helpers';

export default class GoalTarget extends React.Component {
    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
    };

    static HEADING = 'Set Your Goal Deadline';

    state = {
        showCalendar: false,
    };

    onChange(date) {
        this.props.onChange({goalTarget: date.format('YYYY-MM-DD')}, true);
    }

    componentDidUpdate() {
        if (this.state.showCalendar) {
            setHeading('Pick Your Own Date');
        } else {
            setHeading(GoalTarget.HEADING);
        }
    }

    render() {
        let selected;

        if (this.props.data && this.props.data.goalTarget) {
            selected = moment(this.props.data.goalTarget);
        }

        const today = moment(moment().format('YYYY-MM-DD'));

        const suggestion = weeks => {
            const target = moment(today).add({weeks});

            let className = `suggestion suggestion--${weeks} flatButton`;

            if (selected && selected.isSame(target)) {
                className += ' flatButton--selected';
            }

            return (
                <a className={className} onClick={() => this.onChange(target)}>
                    <div className="flatButton__content">
                        <h3>{weeks} Week{weeks > 1 ? 's' : null}</h3>
                        <h5>{target.format('ddd MMM Do')}</h5>
                    </div>
                </a>
            );
        };

        let content;
        let customDate;

        if (this.state.showCalendar) {
            customDate = true;
            content = (
                <div>
                    <DatePicker inline
                                minDate={moment(today).add(1, 'days')}
                                selected={selected}
                                onChange={this.onChange.bind(this)}/>
                </div>
            );
        }
        else {
            customDate = false;
            content = (
                <div className="suggestions">
                    {suggestion(1)}
                    {suggestion(2)}
                    {suggestion(3)}
                    {suggestion(4)}
                    <div style={{clear: 'both'}}/>
                    <a className="flatButton custom"
                       onClick={() => this.setState({showCalendar: true})}>
                        <div className="flatButton__content">
                            <h3>Pick my own date</h3>
                        </div>
                    </a>
                </div>
            );
        }

        return (
            <div className="goalTarget">
                <section>
                    <p>
                        Don’t pick a deadline that makes your goal too easy or too hard to reach. If
                        it seems easy-peasy – stretch yourself more. If it feels like mission
                        impossible, be nicer to yourself!
                    </p>
                    <p>I want to achieve my goal {customDate ? 'by' : 'in'}:</p>
                </section>

                {content}
            </div>
        );
    }
}
