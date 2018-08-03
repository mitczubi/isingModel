import java.awt.Color.*;

public class Ising {
  private int N; // for an NxN lattice
  private double J = 1.0; //strength of spin interaction
  private double kT;//temperature
  private boolean[][] spin; //up (true) and down (false)

  public Ising(int N, double kT, double p) {
    this.N = N;
    this.kT = kT;
    this.spin = new boolean[N][N];

    for (int i = 0; i < N; i++) {
      for (int j = 0; j < N; j++) {
        spin[i][j] = (Math.random() < p); // populating the N x N matrix
      }
    }
  }
  //finding the magnetization based on the boolean array
  public double magnetization() {
    int M = 0;
    for (int i = 0; i < N; i++) {
      for (int j =0; j < N; j++) {
        if (spin[i][j]) M++;
        else            M--;
      }
    }
    return 1.0 * M / (N * N);
  }
  //determining the energy at each location
  private double energy(int i, int j) {
    double E = 0.0;
    if (spin[i][j] == spin[(i+1)%N][j]) E++;
    else                                E--;
    if (spin[i][j] == spin[i][(j+1)%N]) E++;
    else                                E--;
    if (spin[i][j] == spin[(i-1+N)%N][j]) E++;
    else                                E--;
    if (spin[i][j] == spin[i][(j-1+N)%N]) E++;
    else                                E--;

    return -J * E;
  }
  //finding the total energy
  public double energy() {
    double E = 0.0;
    for (int i = 0; i < N; i++) {
      for(int j = 0; j < N; j++) {
        E += 0.5 * energy(i, j);
      }
    }
    return E;
  }
  //one monte Carlo step
  public void step(int i, int j) {
    double deltaE = -2 * energy(i, j);
    //flip the spin if the energy is below zero or get lucky
    if ((deltaE<=0) || (Math.random() <= Math.exp(-deltaE / kT)))
      spin[i][j] = !spin[i][j];
  }
  // one monte carlo step - N^2 times
  public void phase() {
    for (int steps = 0; steps < N*N; steps++) {
      int i = (int) (Math.random() * N);
      int j = (int) (Math.random() * N);
      step(i, j);
    }
  }
  // now we plot the array
  public void draw() {
    for (int i = 0; i < N; i++) {
      for (int j = 0; j < N; j++) {
        if (spin[i][j]) StdDraw.setPenColor(StdDraw.RED);
        else            StdDraw.setPenColor(StdDraw.BLUE);
        StdDraw.filledSquare(i + 0.5, j + 0.5, .5);
      }
    }
    StdDraw.setPenColor(StdDraw.BLACK);
    for (int i = 0; i < N; i++) {
      StdDraw.line(i, 0, i, N);
      StdDraw.line(0, i, N, i);
    }
  }
// string representation
  public String toString() {
    String NEWLINE = System.getProperty("line.separator");
    String s = "";
    for (int i = 0; i < N; i++) {
      for (int j = 0; j < N; j++) {
        if (spin[i][j]) s += "< ";
        else            s += "> ";
        }
        s += NEWLINE;
      }
    return s;
  }
  // main
  public static void main(String[] args) {
    int N = Integer.parseInt(args[0]);
    double kT = Double.parseDouble(args[1]);
    Ising ising = new Ising(N, kT, 0.5);

    StdDraw.setXscale(0, N);
    StdDraw.setYscale(0, N);
    //StdDraw.enableDoubleBuffering();

    for (int t = 0; true; t++){
      ising.phase();
      ising.draw();
      StdDraw.show(20);
      //StdDraw.pause(50);
    }
  }

}
