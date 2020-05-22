import java.io.BufferedReader;
import java.lang.Math;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.HashMap;
import java.util.Arrays;
import java.util.Iterator;
import java.net.Socket;
import java.time.LocalDateTime;
import java.lang.Thread;
import java.util.ArrayList;
import java.util.regex.Pattern;
import java.util.StringTokenizer;

public class hiloServidor implements Runnable {

	PrintStream  p; //Canal de escritura
    BufferedReader  b; //Canal de Lectura
    Socket  cliente; //Socket cliente
    LocalDateTime inicio,fin;
    int numJugadores=0,jugadores=0;
    boolean bandera=false;
    Personajes tablero;
    ThreadGroup grupo;
    int ganador;
    ArrayList<String> excluidos; //Lista de personajes excluidos por el cliente

	
	public hiloServidor(Socket socket,Personajes t,ThreadGroup g, int j){
		this.cliente=socket;
		this.tablero=t;
        this.grupo=g;
        this.numJugadores=j;
        this.ganador=tablero.ganador;
        this.excluidos=new ArrayList<String>();
        try{
            this.b = new BufferedReader ( new InputStreamReader  ( cliente.getInputStream() ) );
            this.p = new PrintStream  ( cliente.getOutputStream() );
        }catch(IOException e){
            System.out.println(e.getMessage());
        }
	}
    public void imprimeTablero(){
        p.println("Lista de caracteristicas de los personajes: ");
        for (int i=0;i<10;i++){
            if(!excluidos.contains(String.valueOf(i))){
                 p.println("Personaje "+i+ ": "+Arrays.toString(tablero.personajes.get(Integer.toString(i)).toArray()));
            } 
        }
    }
    public void dimeComando(String comando){
        StringTokenizer tokenizer= new StringTokenizer(comando.toLowerCase());
        if(Pattern.matches("el personaje es .*",comando.toLowerCase())){
            p.println("Has realizado una jugada");
            while(tokenizer.hasMoreTokens()){
                if(tokenizer.nextToken().equals("es")){
                    if(Integer.parseInt(tokenizer.nextToken())==this.ganador){
                        p.println("Has ganado el juego");
                        break;
                    }
                }
            }

        }else if(Pattern.matches("bloquea a .*", comando.toLowerCase())){
            p.println("Has escogido el comando de bloqueo");
            while(tokenizer.hasMoreTokens()){
                if(tokenizer.nextToken().equals("a")){
                    excluidos.add(tokenizer.nextToken());
                    break;
                }
            }
        }else if(Pattern.matches("el personaje tiene .*", comando.toLowerCase())){
            p.println("has hecho una pregunta");
            while(tokenizer.hasMoreTokens()){
                if(tokenizer.nextToken().equals("tiene")){
                    System.out.println(tokenizer.nextToken());
                }
            }
        }else{
            p.println("comando no encontrado");
        }


    }
	

	public void run(){
        //tab.addObserver(this);
        //imprimeTablero(tab.getTablero().toString());
        String mensaje="";
        p.println("Bienvenido Espera tu turno\n");
        try{
        	inicio = LocalDateTime.now();
            while (true){
                synchronized(tablero){
                    if(grupo.activeCount()<numJugadores && bandera!=true){
                        p.println("Esperando a todos los jugadores");
                        p.println("Jugadores actualmente conectados: "+grupo.activeCount());
                        p.println("Jugadores necesarios para el inicio del juego: "+numJugadores);
                        bandera=true;
                        tablero.wait();
                        //tab.tablero.notify();
                    }
                    if((grupo.activeCount()==numJugadores && numJugadores>1) && bandera==false){
                        p.println("Hay un jugador antes que tu, por favor espera tu turno");
                        tablero.notify();
                        bandera=true;
                        tablero.wait();
                    }
                    /*
                    Dentro de esta función se imprimen los personajes que el cliente no ha excluido
                    */
                    imprimeTablero();
                    p.println("Haga su jugada:");
                    //aquí se recibe el audio del cliente y se le hace su tratamiento
                    mensaje=b.readLine();
                    if(mensaje.equals("by")){
                        break;
                    }
                    dimeComando(mensaje);
                    tablero.notify();
                    /*
                    Si el cliente pide ocultarle un personaje entonces se agrega a su cola de excluidos y no se le imprime más
                    En otro caso se procede con normalidad:
                    Aquí se le responde al cliente si su jugada es correcta o no
                    checaJugada();

                    */
                    if(grupo.activeCount()>1){
                        tablero.wait();
                    }   
                }
                    //break;
            }
            p.println("Hasta luego");
        	p.close();
        	b.close();
        	this.cliente.close();
        }catch(InterruptedException e){
            System.out.println(e.toString());
        }catch(IOException e){
            System.out.println(e.toString());
            System .out.println("No puedo crear el socket");
        }
	}

}