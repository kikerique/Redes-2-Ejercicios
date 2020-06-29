//********************************************************************************************************************************//
//              Ejercicio P2P de Búsqueda de motifs -- Romero Godinez José Enrique-García Mendoza José Luis -- 3CM8               //
//                                                                                                                                //
//   -Los motifs son patrones de bases nitrogenadas o proteinas que se encuentran en una zona de interés del adn, el problema     //
//    computacional que implica su búsqueda lo hace una tarea un tanto complicada ya que algunas zonas de interes cuentan con     //
//    cientos o miles de componentes y por lo regular los motifs buscados tienen una longitud muy pequeña en comparación, además  //
//    de que estos pueden sufrir alteraciones en algunas posiciones por lo que se complica todavía más esta búsqueda.             //
//                                                                                                                                //
//    Nuestra propuesta se basa en un modelo descentralizado de nodos que se conecten entre sí para poder distribuir el trabajo   //
//    de búsqueda de motifs con un enfoque tipo blockchain en el que las solicitudes se agregan a una lista de transacciones con  //
//    todos los datos necesarios para realizar una busqueda y todos los nodos puedan realizar una o más busquedas y al final      //
//    agregarlas a una cadena de respuestas disponible para todos los nodos.                                                      //
//                                                                                                                                //
//    Funcionalidades:                                                                                                            //
//     -La busqueda la realiza cada nodo con un algoritmo greedy que retorna el conjunto de motifs encontrado para una colección  //
//      de kmers de adn así como su puntaje (manera en la que se califica el conjunto de motifs encontrados, a mayor número mejor //
//      conjunto de motifs).                                                                                                      //
//     - Los peers se conectan a un servidor que recibe peticiones http donde se realiza el procesado de los datos y después se   //
//       agregan los resultados a una blockchain disponible para todos los peers conectados.                                      //
//     -Varios servidores pueden conectarse entre sí (por ende también sus nodos) y de esta manera conectar más peers para        //
//      ejecutar la búsqueda.                                                                                                     //
//     -Las peticiones de búsqueda sólo las puede realizar el nodo que tenga usuario y contraseña correctos, para el procesado de //
//      los datos no es necesario esto.                                                                                           //
//                                                                                                                                //
//    Instalación de los requerimientos:                                                                                          // 
//     -Ejecutar el comando pip(3) install -r requirements.txt                                                                    //
//                                                                                                                                //
//    Ejecutar la aplicación:                                                                                                     //
//     -Para ejecutar el servidor http ejecutar los siguientes comandos:                                                          //
//       export FLASK_APP=node_server.py                                                                                          //
//       flask run --host (Host del server) --port (Port del server)                                                              //
//     -Para ejecutar los peers:                                                                                                  //
//       python3 run_app.py (HOST) (PORT) (Host del server) (Port del server)                                                     //
//     -Para conectar dos servidores realizar la siguiente petición http:                                                         //
//       curl -X POST (URLServer1)/register_with -H 'Content-Type: application/json' -d '{"node_address": "(URLServer2"}'         //
//       curl -X POST (URLServer2)/register_with -H 'Content-Type: application/json' -d '{"node_address": "(URLServer1"}'         //
//                                                                                                                                //
//     
//********************************************************************************************************************************//

Dataset:
	DNA kmers:
       GCGCCCCGCCCGGACAGCCATGCGCTAACCCTGGCTTCGATGGCGCCGGCTCAGTTAGGGCCGGAAGTCCCCAATGTGGCAGACCTTTCGCCCCTGGCGGACGAATGACCCCAGTGGCCGGGACTTCAGGCCCTATCGGAGGGCTCCGGCGCGGTGGTCGGATTTGTCTGTGGAGGTTACACCCCAATCGCAAGGATGCATTATGACCAGCGAGCTGAGCCTGGTCGCCACTGGAAAGGGGAGCAACATC
       CCGATCGGCATCACTATCGGTCCTGCGGCCGCCCATAGCGCTATATCCGGCTGGTGAAATCAATTGACAACCTTCGACTTTGAGGTGGCCTACGGCGAGGACAAGCCAGGCAAGCCAGCTGCCTCAACGCGCGCCAGTACGGGTCCATCGACCCGCGGCCCACGGGTCAAACGACCCTAGTGTTCGCTACGACGTGGTCGTACCTTCGGCAGCAGATCAGCAATAGCACCCCGACTCGAGGAGGATCCCG
       ACCGTCGATGTGCCCGGTCGCGCCGCGTCCACCTCGGTCATCGACCCCACGATGAGGACGCCATCGGCCGCGACCAAGCCCCGTGAAACTCTGACGGCGTGCTGGCCGGGCTGCGGCACCTGATCACCTTAGGGCACTTGGGCCACCACAACGGGCCGCCGGTCTCGACAGTGGCCACCACCACACAGGTGACTTCCGGCGGGACGTAAGTCCCTAACGCGTCGTTCCGCACGCGGTTAGCTTTGCTGCC
       GGGTCAGGTATATTTATCGCACACTTGGGCACATGACACACAAGCGCCAGAATCCCGGACCGAACCGAGCACCGTGGGTGGGCAGCCTCCATACAGCGATGACCTGATCGATCATCGGCCAGGGCGCCGGGCTTCCAACCGTGGCCGTCTCAGTACCCAGCCTCATTGACCCTTCGACGCATCCACTGCGCGTAAGTCGGCTCAACCCTTTCAAACCGCTGGATTACCGACCGCAGAAAGGGGGCAGGAC
       GTAGGTCAAACCGGGTGTACATACCCGCTCAATCGCCCAGCACTTCGGGCAGATCACCGGGTTTCCCCGGTATCACCAATACTGCCACCAAACACAGCAGGCGGGAAGGGGCGAAAGTCCCTTATCCGACAATAAAACTTCGCTTGTTCGACGCCCGGTTCACCCGATATGCACGGCGCCCAGCCATTCGTGACCGACGTCCCCAGCCCCAAGGCCGAACGACCCTAGGAGCCACGAGCAATTCACAGCG
       CCGCTGGCGACGCTGTTCGCCGGCAGCGTGCGTGACGACTTCGAGCTGCCCGACTACACCTGGTGACCACCGCCGACGGGCACCTCTCCGCCAGGTAGGCACGGTTTGTCGCCGGCAATGTGACCTTTGGGCGCGGTCTTGAGGACCTTCGGCCCCACCCACGAGGCCGCCGCCGGCCGATCGTATGACGTGCAATGTACGCCATAGGGTGCGTGTTACGGCGATTACCTGAAGGCGGCGGTGGTCCGGA
       GGCCAACTGCACCGCGCTCTTGATGACATCGGTGGTCACCATGGTGTCCGGCATGATCAACCTCCGCTGTTCGATATCACCCCGATCTTTCTGAACGGCGGTTGGCAGACAACAGGGTCAATGGTCCCCAAGTGGATCACCGACGGGCGCGGACAAATGGCCCGCGCTTCGGGGACTTCTGTCCCTAGCCCTGGCCACGATGGGCTGGTCGGATCAAAGGCATCCGTTTCCATCGATTAGGAGGCATCAA
       GTACATGTCCAGAGCGAGCCTCAGCTTCTGCGCAGCGACGGAAACTGCCACACTCAAAGCCTACTGGGCGCACGTGTGGCAACGAGTCGATCCACACGAAATGCCGCCGTTGGGCCGCGGACTAGCCGAATTTTCCGGGTGGTGACACAGCCCACATTTGGCATGGGACTTTCGGCCCTGTCCGCGTCCGTGTCGGCCAGACAAGCTTTGGGCATTGGCCACAATCGGGCCACAATCGAAAGCCGAGCAG
       GGCAGCTGTCGGCAACTGTAAGCCATTTCTGGGACTTTGCTGTGAAAAGCTGGGCGATGGTTGTGGACCTGGACGAGCCACCCGTGCGATAGGTGAGATTCATTCTCGCCCTGACGGGTTGCGTCTGTCATCGGTCGATAAGGACTAACGGCCCTCAGGTGGGGACCAACGCCCCTGGGAGATAGCGGTCCCCGCCAGTAACGTACCGCTGAACCGACGGGATGTATCCGCCCCAGCGAAGGAGACGGCG
       TCAGCACCATGACCGCCTGGCCACCAATCGCCCGTAACAAGCGGGACGTCCGCGACGACGCGTGCGCTAGCGCCGTGGCGGTGACAACGACCAGATATGGTCCGAGCACGCGGGCGAACCTCGTGTTCTGGCCTCGGCCAGTTGTGTAGAGCTCATCGCTGTCATCGAGCGATATCCGACCACTGATCCAAGTCGGGGGCTCTGGGGACCGAAGTCCCCGGGCTCGGAGCTATCGGACCTCACGATCACC
    Kmer length:
       15
       
    Respuesta:
       
       ['GTTAGGGCCGGAAGT', 'CCGATCGGCATCACT', 'ACCGTCGATGTGCCC', 'GGGTCAGGTATATTT', 'GTGACCGACGTCCCC', 'CTGTTCGCCGGCAGC', 'CTGTTCGATATCACC', 'GTACATGTCCAGAGC', 'GCGATAGGTGAGATT', 'CTCATCGCTGTCATC']

	   64

