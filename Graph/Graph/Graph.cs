using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace Graph
{
    class Node<T>
    {
        public T Value;
        public IDictionary<Node<T>, uint> Neighbours = new Dictionary<Node<T>, uint>();

        public Node(T vertex)
        {
            Value = vertex;
        }
    }

    public class Graph<T> : IGraph<T>
    {
        private IDictionary<T, Node<T>> nodes = new Dictionary<T, Node<T>>();

        public void Add(T vertex)
        {
            nodes[vertex] = new Node<T>(vertex);
        }

        public void Connect(T a, T b, uint weight)
        
        {
            nodes[a].Neighbours[nodes[b]] = weight;
        }

        public uint Path(T @from, T to)
        {
            var paths = new Dictionary<T, uint> {{from, 0}};
            var traversal = new Queue<Node<T>>();
            traversal.Enqueue(nodes[from]);
            while (traversal.Count > 0)
            {
                var current = traversal.Dequeue();
                foreach (var (node, w) in current.Neighbours)
                {
                    var totalWeight = w + paths[current.Value];     
                    var exists = paths.TryGetValue(node.Value, out var prevPath);
                    if (!exists || prevPath > totalWeight)
                    {
                        paths[node.Value] = totalWeight;
                    }

                    if (!exists)
                    {
                        traversal.Enqueue(node);
                    }
                }
            }
            return paths[to];
        }

        public IEnumerator<T> GetEnumerator() {
            return nodes.Select(kvp => kvp.Key).GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator() {
            return GetEnumerator();
        }
    }
}
