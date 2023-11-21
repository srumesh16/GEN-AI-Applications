/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";

interface Props {
  color: string;
  className: any;
}

export const LayersThree01 = ({ color = "white", className }: Props): JSX.Element => {
  return (
    <svg
      className={`layers-three-01 ${className}`}
      fill="none"
      height="24"
      viewBox="0 0 24 24"
      width="24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        className="path"
        clipRule="evenodd"
        d="M1.10557 11.5528C1.35256 11.0588 1.95324 10.8586 2.44721 11.1056L12 15.882L21.5528 11.1056C22.0468 10.8586 22.6474 11.0588 22.8944 11.5528C23.1414 12.0468 22.9412 12.6474 22.4472 12.8944L12.805 17.7155C12.7976 17.7192 12.789 17.7236 12.7794 17.7285C12.6861 17.7761 12.493 17.8747 12.2766 17.9153C12.0938 17.9496 11.9062 17.9496 11.7234 17.9153C11.507 17.8747 11.3139 17.7761 11.2206 17.7285C11.211 17.7236 11.2024 17.7192 11.195 17.7155L1.55279 12.8944C1.05881 12.6474 0.858584 12.0468 1.10557 11.5528Z"
        fill={color}
        fillRule="evenodd"
      />
      <path
        className="path"
        clipRule="evenodd"
        d="M1.10557 16.5528C1.35256 16.0588 1.95324 15.8586 2.44721 16.1056L12 20.882L21.5528 16.1056C22.0468 15.8586 22.6474 16.0588 22.8944 16.5528C23.1414 17.0468 22.9412 17.6474 22.4472 17.8944L12.805 22.7155C12.7976 22.7192 12.789 22.7236 12.7794 22.7285C12.6861 22.7761 12.493 22.8747 12.2766 22.9153C12.0938 22.9496 11.9062 22.9496 11.7234 22.9153C11.507 22.8747 11.3139 22.7761 11.2206 22.7285C11.211 22.7236 11.2024 22.7192 11.195 22.7155L1.55279 17.8944C1.05881 17.6474 0.858584 17.0468 1.10557 16.5528Z"
        fill={color}
        fillRule="evenodd"
      />
      <path
        className="path"
        clipRule="evenodd"
        d="M11.7234 1.08474C11.9062 1.05044 12.0938 1.05044 12.2766 1.08474C12.493 1.12535 12.6861 1.22388 12.7794 1.27149C12.789 1.27639 12.7976 1.28075 12.805 1.28446L22.4472 6.10557C22.786 6.27496 23 6.62123 23 7C23 7.37877 22.786 7.72504 22.4472 7.89443L12.805 12.7155C12.7976 12.7192 12.789 12.7236 12.7794 12.7285C12.6861 12.7761 12.493 12.8747 12.2766 12.9153C12.0938 12.9496 11.9062 12.9496 11.7234 12.9153C11.507 12.8747 11.3139 12.7761 11.2206 12.7285C11.211 12.7236 11.2024 12.7192 11.195 12.7155L1.55279 7.89443C1.214 7.72504 1 7.37877 1 7C1 6.62123 1.214 6.27496 1.55279 6.10557L11.195 1.28446C11.2024 1.28075 11.211 1.27639 11.2206 1.27149C11.3139 1.22388 11.507 1.12535 11.7234 1.08474Z"
        fill={color}
        fillRule="evenodd"
      />
    </svg>
  );
};

LayersThree01.propTypes = {
  color: PropTypes.string,
};