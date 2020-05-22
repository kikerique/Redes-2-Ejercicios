import java.util.Scanner;
import java.io.BufferedReader;
import java.lang.Math;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.InetSocketAddress;
import java.net.InetAddress;
import java.lang.Thread;
import java.io.IOException;
import java.util.Arrays;

public class Servidor {
    Socket  cliente; //Socket cliente
    PrintStream  p; //Canal de escritura
    BufferedReader  b; //Canal de Lectura
    Personajes tablero;


    /*
       void iniciaServer(String HOST,int PORT,int numeroConexiones)
        Método que crea un objeto de tipo Server Socket en la dirección ip y puertos especificados
        y se queda a la espera de nuevas conexiones
    */
    
    public void iniciaServer(String HOST,int PORT,int numeroConexiones){
        ThreadGroup principiantes;
        Thread hilo;
        int conexionesActivasp=0;
        Runnable nuevoCliente;
        ServerSocket  s; //Socket servidor
        Socket  sc; //Socket cliente
        principiantes=new ThreadGroup("principiantes");
        tablero=new Personajes();
        System.out.println("El ganador es :"+ tablero.ganador);
        try {
            //Creo el socket server
            s = new ServerSocket (PORT,numeroConexiones,InetAddress.getByName(HOST));
            
            System.out.println("Servidor escuchando en la IP: "+s.getInetAddress().toString());
            System.out.println("Servidor escuchando en el puerto: "+s.getLocalPort());
            while ( true ) {
                //Invoco el metodo accept del socket servidor, me devuelve una referencia al socket cliente
                sc = s.accept();
                conexionesActivasp=principiantes.activeCount();
                p = new PrintStream  ( sc.getOutputStream() );
                nuevoCliente = new hiloServidor(sc,tablero,principiantes,numeroConexiones);
                hilo=new Thread(principiantes,nuevoCliente);    
                if((conexionesActivasp)<numeroConexiones){
                        hilo.start();
                        //conexionesActivasp=principiantes.activeCount();
                }else{
                        p.println("Servidor lleno");
                        p.println("Hasta luego");
                        sc.close();
                }
                
                    //hilo.start();
                    //System.out.println("gg: " +nuevoCliente.activeCount());

                    //conexionesActivas--; 
            }
            
        } catch (IOException  e) {
            System.out.println(e.toString());
            System .out.println("No puedo crear el socket");
        }
    }


    public static void main(String [] args) {
        if(args.length<3){
            System.out.println("Uso: java ejecutable HOST PORT #conexiones-permitidas");
        }else{
            Servidor s=new Servidor();
            s.iniciaServer(args[0],Integer.parseInt(args[1]),Integer.parseInt(args[2]));
        }
    }

}