import React from "react";
import './styles.scss';

export class Loading extends React.Component {
    render() {
        const style = {background: this.props.color};
        return (
            <div className="loading">
                <div className="anim-box">
                    {[...Array(3).keys()].map((_, index) => (
                        <div key={index} style={style} className="circle"/>
                    ))}
                </div>
            </div>
        );
    }
}
