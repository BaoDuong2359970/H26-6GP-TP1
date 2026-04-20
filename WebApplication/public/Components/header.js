class Header extends HTMLElement {
  constructor() {
    super();
  }

connectedCallback() {
    this.innerHTML = `
      <style>
        nav {
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        ul {
          padding: 0;
        }

        a {
          font-weight: 700;
          margin: 0 25px;
          color: #000000;
          text-decoration: none;
        }

        a:hover {
          padding-bottom: 5px;
          box-shadow: inset 0 -2px 0 0 #1f2e1b;
        }
      </style>
      <header>
        <nav>
          <ul>
            <li><a href="index.html">Control Pannel</a></li>
            <li><a href="history.html">History of logs</a></li>
          </ul>
        </nav>
      </header>
    `;
  }
}

customElements.define('header-component', Header);