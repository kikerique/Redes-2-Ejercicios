import java.util.ArrayList;
import java.util.HashMap;
import java.util.Arrays;
public class Personajes{
	HashMap<String,ArrayList<String>> personajes;
	int ganador;
	final String[][] fisicas={
							{"Azul","Negro","Amarillo","Rojo","Cafe","Violeta","Gris","Verde","Calvo","Rosa"}, //Color de pelo
							{"Delgado","Flaco","Gordo","Morbido","Atletico","Robusto","Muy Atletico","Esqueletico","Normal","Amorfo"}, //Complexión
							{"Alto","Bajo","Enano","Gigante","Godzilla","Liliputiense","Microscopico","Planeta","Subatomico","Enorme"},//Estatura
							{"Blanco","Cafe","Negro","Rojo","Azul","Verde","Morado","Rosa","Amarillo","Carton"},//Color de piel
							{"Humano","Monstruo","Saiyajin","Depredador","Robot","Reptiliano","Atlante","Hombre pez","Alien","Marciano"}//Raza
							};
	final String[][] sobresalientes={
							{"Arquitectura","Cine","Pintura","Escultura","Poesia","Musica","Danza"}, //Artes
							{"Football","Baseball","Basquetball","Soccer","Esports","Rugby","Archery"}, //Deportes
							{"Química","Fisica","Biologia","Computacion","Fisica Cuantica","Epidemiologia","Farmacologia"},//Ciencia
							{"Licenciado","Ingeniero","Maestro","Doctor","Postdoctor","Bachiller","Lider Supremo"},//Grado
							{"Puzzles","Acuarios","Terrarios","Legos","Caminata","Maquetas","Dormir"}//Hobby
							};		
	public Personajes(){
		this.personajes=new HashMap<String,ArrayList<String>>(10);
		generaCaracteristicas();
		ganador=(int)Math.floor(Math.random()*11);
	}

	public void generaCaracteristicas(){
		ArrayList<String> caracteristicas;
		double numero,numero2;
		//Genera un numero random para escoger las caracteristicas
		numero=Math.random();
		for(int i=0;i<10;i++){
			caracteristicas=new ArrayList<String>(5);
			for(int k=0;k<5;k++){
				if(numero>0.5){
					//Genera un numero random de 0 a tipoCaracteristicas.length()-1
					numero2=Math.random()*fisicas[k].length;
					caracteristicas.add(fisicas[k][(int)numero2]);
				}else{
					//Genera un numero random de 0 a tipoCaracteristicas.length()-1
					numero2=Math.random()*sobresalientes[k].length;
					caracteristicas.add(sobresalientes[k][(int)numero2]);
				}
				
			}
			//System.out.println(Arrays.toString(caracteristicas.toArray()));
			this.personajes.put(Integer.toString(i),caracteristicas);
		}

	}

	public ArrayList<String> getGanador(){
		return personajes.get(Integer.toString(this.ganador));
	}
	/*public static void main(String args[]){
		Personajes lista=new Personajes();
		ArrayList<String> caracteristicasGanador=lista.getGanador();
		System.out.println("Lista de caracteristicas de los personajes: ");
		for (int i=0;i<10;i++){
			System.out.println("Personaje "+i+ ": "+Arrays.toString(lista.personajes.get(Integer.toString(i)).toArray()));
		}
		System.out.println("Lista de caracteristicas del Personaje ganador");
		System.out.println(Arrays.toString(caracteristicasGanador.toArray()));
	}*/
}