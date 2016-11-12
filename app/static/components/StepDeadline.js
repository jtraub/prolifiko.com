import React from 'react';
import moment from 'moment';
import DatePicker from 'react-datepicker';
import { setHeading } from '../helpers';

export default class StepDeadline extends React.Component {
    static HEADING = 'Set Your Step Deadline';

    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
        data: React.PropTypes.object.isRequired,
    };

    static defaultProps = {
        data: {
            stepDeadline: moment().add(1, 'days').format('YYYY-MM-DD'),
        }
    };

    state = {
        showCalendar: false,
    };

    onChange(date) {
        this.props.onChange({stepDeadline: date.format('YYYY-MM-DD')}, true);
    }

    componentDidUpdate() {
        if (this.state.showCalendar) {
            setHeading('Pick Your Own Date');
        } else {
            setHeading(StepDeadline.HEADING);
        }
    }

    render() {
        const selected = moment(this.props.data.stepDeadline);

        const today = moment(moment().format('YYYY-MM-DD'));

        const suggestion = days => {
            const target = moment(today).add({days});

            let className = `suggestion suggestion--${days} flatButton`;

            if (selected && selected.isSame(target)) {
                className += ' flatButton--selected';
            }

            return (
                <a className={className} onClick={() => this.onChange(target)}>
                    <div className="flatButton__content">
                        <h3>{days} Day{days > 1 ? 's' : null}</h3>
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
                    <a className="flatButton custom"
                       onClick={() => this.setState({showCalendar: false})}>
                        <div className="flatButton__content">
                            <h3>Pick a set date</h3>
                        </div>
                    </a>
                </div>
            );
        } else {
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
            <div>
                <section>
                    <p>Don't pick a deadline that makes your goal too easy or too hard to reach. If
                        it
                        seems easy-peasy – stretch yourself more. If it feels like mission
                        impossible, be
                        nicer to yourself!</p>
                </section>

                {content}
            </div>
        );
    }
}
