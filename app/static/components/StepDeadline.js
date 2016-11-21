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
        showCalendar: false
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
        let selected;

        if (this.props.data && this.props.data.stepDeadline) {
            selected = moment(this.props.data.stepDeadline);
        }

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
        let intro;

        if (this.props.stepNumber === 1) {
            intro = <p>I want to achieve my first step:</p>;
        } else {
            intro = <p>I want to achieve my step:</p>;
        }

        if (this.state.showCalendar) {
            content = (
                <div>
                    <DatePicker inline
                                minDate={moment(today).add(1, 'days')}
                                selected={selected}
                                onChange={this.onChange.bind(this)}/>
                </div>
            );

            intro = <p>I want to achieve my step by:</p>;
        } else {
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
                <section>{intro}</section>
                {content}
            </div>
        );
    }
}
