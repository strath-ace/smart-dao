import React from "react";

export function RefreshNotifications({userAddress, update_page}) {
    return (
          <form
            onSubmit={(event) => {
              // This function just calls the transferTokens callback with the
              event.preventDefault();
              update_page(userAddress);
            }}
          >
            <button id="refresh-btn" type="submit"><img src="/refresh.png" alt="Refresh Button"/></button>
          </form>
      );
}