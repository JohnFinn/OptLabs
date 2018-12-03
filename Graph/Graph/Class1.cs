using System.Collections;
using System.Collections.Generic;

namespace Graph{
    public interface IGraph<T> : IEnumerable<T>
    {
        void Add(T vertex);
        void Connect(T a, T b, uint weight);
        uint Path(T from, T to);
    }
}
