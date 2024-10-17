# Elevator Simulation Project

## Overview

The Elevator Simulation Project is a Python-based application that models and visualizes the operation of two elevators within a multi-floor building. Utilizing Pygame for the graphical user interface and integrating neural networks for decision-making, this project aims to simulate realistic elevator behavior, optimize elevator dispatching, and enhance passenger satisfaction.

## Features

- **Graphical Interface:** Real-time visualization of elevator movements, floor statuses, and passenger distribution using Pygame.
- **Neural Network Integration:** Implements neural networks to manage elevator actions based on current state and passenger requests.
- **Simulation Loop:** Runs continuous simulations to test and improve elevator algorithms.
- **Data Generation:** Generates synthetic passenger data to simulate various elevator scenarios.
- **Animation:** Smooth animations for elevator operations, including door movements and passenger boarding.

## Installation

### Prerequisites

- Python 3.6 or higher
- Pygame
- PyTorch

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/elevator-simulation.git
   cd elevator-simulation
   ```

2. **Create a Virtual Environment (Optional but Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *If `requirements.txt` is not present, you can install the necessary packages manually:*

   ```bash
   pip install pygame torch
   ```

4. **Prepare Assets:**

   Ensure that the images for elevators, persons, and floors are placed in the project directory or update the paths in `ui.py` accordingly.

## Usage

1. **Run the Simulation:**

   ```bash
   python main.py
   ```

   This will start the simulation using the `main.py` script, which loads the neural network weights and begins the elevator animation.

2. **Customize Parameters:**

   - **Passenger Data:** Modify `andygenlist.py` or the passenger list in `main.py` to simulate different numbers of passengers and floor configurations.
   - **Neural Network Weights:** Update or retrain the neural network as needed by modifying the `loadweights` and `saveweights` functions in `main.py`.

3. **Visualize Elevator Operations:**

   The Pygame window will display the elevators moving between floors, doors opening/closing, and passengers boarding/alighting.

## File Structure

- **`ui.py`:** Handles the graphical user interface using Pygame, including loading images and rendering elevator animations.
- **`main.py`:** Entry point of the application. Manages simulation parameters, loads neural network weights, and initiates the animation.
- **`animation.py`:** Contains functions related to updating and animating the elevator states.
- **`simulation.py`:** Handles the simulation logic, including passenger generation and elevator decision-making.
- **`andygenlist.py`:** Generates random passenger data for simulation.
- **`.vscode/launch.json`:** Configuration file for debugging with Visual Studio Code.
- **Other Files:**
  - **`gradient5.txt`:** Presumably contains gradient data or neural network weights.
  - **`paslist.txt`:** Stores passenger lists generated for simulations.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**
2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Pygame](https://www.pygame.org/) for providing the tools to create the graphical interface.
- [PyTorch](https://pytorch.org/) for facilitating the integration of neural networks.

---

Happy Simulating!