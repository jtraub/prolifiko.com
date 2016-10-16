import React from 'react';
import moment from 'moment';
import DatePicker  from 'react-datepicker';

export default class GoalTarget extends React.Component {
    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
    };

    state = {
        showCalendar: false,
    };

    onChange(date) {
        this.props.onChange({goalTarget: date.format('YYYY-MM-DD')}, true);
    }

    render() {
        let selected;

        if (this.props.data) {
            selected = moment(this.props.data.goalTarget);
        }

        const today = moment(moment().format('YYYY-MM-DD'));

        const suggestion = days => {
            const target = moment(today).add({ days });

            let className = `suggestion suggestion--${days} flatButton`;

            if (selected && selected.isSame(target)) {
                className += ' flatButton--selected';
            }

            return (
                <a className={className} onClick={() => this.onChange(target)}>
                    <div className="flatButton__content">
                        <h3>{days} Days</h3>
                        <h5>{target.format('ddd MMM Do')}</h5>
                    </div>
                </a>
            );
        };

        let content;

        if (this.state.showCalendar) {
            content = <DatePicker inline minDate={moment(today).add(1, 'days')} selected={selected} onChange={this.onChange.bind(this)}/>;
        } else {
            content = (
                <div className="suggestions">
                    {suggestion(5)}
                    {suggestion(7)}
                    {suggestion(10)}
                    {suggestion(30)}
                    <div style={{ clear: 'both' }}/>
                    <a className="flatButton custom" onClick={() => this.setState({ showCalendar: true })}>
                        <div className="flatButton__content">
                            <h3>Pick my own</h3>
                        </div>
                    </a>
                </div>
            );
        }

        return (
            <div className="goalTarget">
                <section>
                    <p>Next you need to decide when you'd like to achieve this goal by.</p>

                    <p>We suggest you target 5-10 days.</p>
                </section>

                {content}
            </div>
        );
    }
}
